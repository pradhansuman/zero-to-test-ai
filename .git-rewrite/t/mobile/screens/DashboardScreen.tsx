import React, { useState, useEffect } from 'react';
import {
  View,
  ScrollView,
  Text,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  FlatList,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { apiClient } from '../services/apiClient';

export default function DashboardScreen() {
  const [metrics, setMetrics] = useState(null);
  const [executions, setExecutions] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigation = useNavigation();

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const projectId = 1; // From context
      const response = await apiClient.get(`/analytics/dashboard/${projectId}`);
      setMetrics(response.data);

      const execResponse = await apiClient.get(`/projects/${projectId}/executions`);
      setExecutions(execResponse.data);
    } catch (error) {
      console.error('Failed to fetch dashboard', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#2563eb" />
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {metrics && (
        <View style={styles.metricsContainer}>
          <Text style={styles.sectionTitle}>Dashboard Metrics</Text>

          <View style={styles.metricCard}>
            <Text style={styles.metricLabel}>Pass Rate</Text>
            <Text style={styles.metricValue}>{metrics.pass_fail_rate}%</Text>
          </View>

          <View style={styles.metricCard}>
            <Text style={styles.metricLabel}>Total Executions</Text>
            <Text style={styles.metricValue}>{metrics.total_executions}</Text>
          </View>

          <View style={styles.metricCard}>
            <Text style={styles.metricLabel}>Avg Duration</Text>
            <Text style={styles.metricValue}>{metrics.avg_duration}s</Text>
          </View>
        </View>
      )}

      <View style={styles.executionsContainer}>
        <Text style={styles.sectionTitle}>Recent Executions</Text>

        {executions.length > 0 ? (
          <FlatList
            scrollEnabled={false}
            data={executions}
            keyExtractor={(item) => item.id.toString()}
            renderItem={({ item }) => (
              <TouchableOpacity
                style={styles.executionCard}
                onPress={() =>
                  navigation.navigate('ExecutionDetail', { executionId: item.id })
                }
              >
                <Text style={styles.executionTitle}>Execution #{item.id}</Text>
                <Text style={styles.executionStatus}>Status: {item.status}</Text>
                <Text style={styles.executionDate}>
                  {new Date(item.created_at).toLocaleDateString()}
                </Text>
              </TouchableOpacity>
            )}
          />
        ) : (
          <Text style={styles.noData}>No executions yet</Text>
        )}
      </View>

      <TouchableOpacity style={styles.runButton}>
        <Text style={styles.runButtonText}>Run Tests</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  metricsContainer: {
    padding: 15,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  metricCard: {
    backgroundColor: '#fff',
    padding: 15,
    marginBottom: 10,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#2563eb',
  },
  metricLabel: {
    color: '#666',
    fontSize: 12,
  },
  metricValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2563eb',
  },
  executionsContainer: {
    padding: 15,
  },
  executionCard: {
    backgroundColor: '#fff',
    padding: 15,
    marginBottom: 10,
    borderRadius: 8,
  },
  executionTitle: {
    fontWeight: 'bold',
    fontSize: 14,
  },
  executionStatus: {
    color: '#666',
    marginTop: 5,
  },
  executionDate: {
    color: '#999',
    fontSize: 12,
    marginTop: 5,
  },
  noData: {
    color: '#999',
    textAlign: 'center',
    padding: 20,
  },
  runButton: {
    backgroundColor: '#2563eb',
    margin: 15,
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  runButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
});
