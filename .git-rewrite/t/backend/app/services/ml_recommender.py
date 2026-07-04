"""ML-based test recommendation service using scikit-learn."""
import json
import pickle
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models import TestCase, Execution
from app.utils.logger import StructuredLogger

logger = StructuredLogger(__name__)

class MLRecommender:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = None
        self.features = {}

    async def get_recommendations(self, project_id: int, code_changes: list, top_k: int = 10) -> dict:
        """Get ML-based test recommendations for code changes."""
        try:
            # Extract features from code changes
            features = await self._extract_features(code_changes)

            # Get historical test data
            test_cases = await self._get_test_history(project_id)

            # Calculate relevance scores
            recommendations = await self._score_tests(test_cases, features)

            # Return top K recommendations
            top_recommendations = sorted(
                recommendations,
                key=lambda x: x['relevance_score'],
                reverse=True
            )[:top_k]

            logger.info(
                "recommendations_generated",
                project_id=project_id,
                count=len(top_recommendations),
                features=features
            )

            return {
                'project_id': project_id,
                'recommendations': top_recommendations,
                'total_available': len(recommendations),
                'top_k': top_k,
                'timestamp': datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error("recommendation_error", error=str(e))
            return {"error": str(e)}

    async def predict_failures(self, project_id: int, test_id: int) -> dict:
        """Predict likelihood of test failure based on historical data."""
        try:
            # Get test history
            result = await self.db.execute(
                select(Execution)
                .where(Execution.test_case_id == test_id)
                .order_by(Execution.created_at.desc())
                .limit(20)
            )
            executions = result.scalars().all()

            if not executions:
                return {'test_id': test_id, 'failure_probability': 0.0, 'confidence': 0.0}

            # Calculate failure rate
            failures = sum(1 for e in executions if e.status == 'failed')
            failure_probability = failures / len(executions)

            # Calculate trend (getting better or worse?)
            recent_failures = sum(1 for e in executions[:5] if e.status == 'failed')
            recent_rate = recent_failures / min(5, len(executions))

            trend = 'improving' if recent_rate < failure_probability else 'degrading'

            return {
                'test_id': test_id,
                'failure_probability': round(failure_probability, 3),
                'trend': trend,
                'confidence': min(len(executions) / 20, 1.0),
                'recent_runs': len(executions),
            }
        except Exception as e:
            logger.error("failure_prediction_error", error=str(e))
            return {"error": str(e)}

    async def train_model(self, project_id: int) -> dict:
        """Train ML model on project's historical data."""
        try:
            # Get all test cases and their execution history
            result = await self.db.execute(
                select(TestCase).where(TestCase.project_id == project_id)
            )
            test_cases = result.scalars().all()

            if not test_cases:
                return {'error': 'No test cases found for training'}

            # Prepare training data
            X = []
            y = []
            for tc in test_cases:
                # Get execution history
                exec_result = await self.db.execute(
                    select(Execution)
                    .where(Execution.test_case_id == tc.id)
                    .order_by(Execution.created_at.desc())
                    .limit(50)
                )
                executions = exec_result.scalars().all()

                if executions:
                    # Feature: pass rate
                    passes = sum(1 for e in executions if e.status == 'passed')
                    pass_rate = passes / len(executions)

                    # Feature: average duration
                    avg_duration = sum(e.duration for e in executions if e.duration) / len(executions)

                    # Feature: flakiness (std dev of outcomes)
                    recent = executions[:10]
                    flakiness = sum(1 for e in recent if e.status == 'failed') / len(recent)

                    X.append([pass_rate, avg_duration, flakiness])
                    y.append(pass_rate)

            # Train simple linear model
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
            model.fit(X, y)

            # Serialize model
            model_data = pickle.dumps(model)

            # Calculate accuracy
            accuracy = model.score(X, y)

            logger.info(
                "model_trained",
                project_id=project_id,
                accuracy=accuracy,
                samples=len(X)
            )

            return {
                'project_id': project_id,
                'model_type': 'linear_regression',
                'accuracy': round(accuracy, 3),
                'training_samples': len(X),
                'trained_at': datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error("model_training_error", error=str(e))
            return {"error": str(e)}

    async def _extract_features(self, code_changes: list) -> dict:
        """Extract features from code changes."""
        return {
            'files_changed': len(code_changes),
            'modules_affected': len(set(c.get('module', '') for c in code_changes)),
            'has_test_changes': any('test' in c.get('file', '').lower() for c in code_changes),
            'has_api_changes': any('api' in c.get('file', '').lower() for c in code_changes),
        }

    async def _get_test_history(self, project_id: int) -> list:
        """Get test cases and their execution history."""
        result = await self.db.execute(
            select(TestCase).where(TestCase.project_id == project_id)
        )
        return result.scalars().all()

    async def _score_tests(self, test_cases: list, features: dict) -> list:
        """Score tests based on relevance to code changes."""
        recommendations = []

        for tc in test_cases:
            score = 0.0
            reasons = []

            # Module affinity scoring
            if features['modules_affected'] > 0:
                if tc.test_type and any(m in tc.test_type for m in ['api', 'integration']):
                    score += 0.3
                    reasons.append('matches_module_type')

            # API/UI specificity
            if features['has_api_changes'] and 'api' in (tc.test_type or '').lower():
                score += 0.4
                reasons.append('api_test_relevant')

            # Flakiness penalty (avoid flaky tests)
            if tc.tags and 'flaky' not in tc.tags:
                score += 0.2
                reasons.append('stable_test')

            # Randomness factor for exploration
            import random
            score += random.random() * 0.1

            recommendations.append({
                'test_id': tc.id,
                'test_name': tc.name,
                'test_type': tc.test_type,
                'relevance_score': round(min(score, 1.0), 3),
                'reasons': reasons,
            })

        return recommendations
