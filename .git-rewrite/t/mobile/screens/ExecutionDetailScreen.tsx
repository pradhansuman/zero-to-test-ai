import React, { useState, useEffect } from 'react';
import {
  View,
  ScrollView,
  Text,
  StyleSheet,
  ActivityIndicator,
} from 'react-native';
import { apiClient } from '../services/apiClient';

export default function ExecutionDetailScreen({ route }) {
  const { executionId } = route.params;
  const [execution, setExecution] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchExecutionDetail();
  }, []);

  const fetchExecutionDetail = async () => {
    try {
      const response = await apiClient.get(`/projects/1/executions/${executionId}`);
      setExecution(response.data);
    } catch (error) {
      console.error('Failed to fetch execution', error);
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

  if (!execution) {
    return (
      <View style={styles.centered}>
        <Text>Execution not found</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Execution #{execution.id}</Text>
        <Text style={[styles.status, { color: execution.status === 'passed' ? '#10b981' : '#ef4444' }]}>
          {execution.status.toUpperCase()}
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Summary</Text>

        <View style={styles.row}>
          <Text style={styles.label}>Total Tests:</Text>
          <Text style={styles.value}>{execution.total_tests || 0}</Text>
        </View>

        <View style={styles.row}>
          <Text style={styles.label}>Passed:</Text>
          <Text style={[styles.value, { color: '#10b981' }]}>{execution.passed || 0}</Text>
        </View>

        <View style={styles.row}>
          <Text style={styles.label}>Failed:</Text>
          <Text style={[styles.value, { color: '#ef4444' }]}>{execution.failed || 0}</Text>
        </View>

        <View style={styles.row}>
          <Text style={styles.label}>Duration:</Text>
          <Text style={styles.value}>{execution.duration || 0}s</Text>
        </View>

        <View style={styles.row}>
          <Text style={styles.label}>Started:</Text>
          <Text style={styles.value}>{new Date(execution.created_at).toLocaleString()}</Text>
        </View>
      </View>

      {execution.error_message && (
        <View style={styles.errorSection}>
          <Text style={styles.errorTitle}>Error Details</Text>
          <Text style={styles.errorText}>{execution.error_message}</Text>
        </View>
      )}
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
  header: {
    backgroundColor: '#fff',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  status: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  section: {
    backgroundColor: '#fff',
    margin: 15,
    padding: 15,
    borderRadius: 8,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  label: {
    color: '#666',
    fontWeight: '500',
  },
  value: {
    fontWeight: 'bold',
    color: '#333',
  },
  errorSection: {
    backgroundColor: '#fee2e2',
    margin: 15,
    padding: 15,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#ef4444',
  },
  errorTitle: {
    color: '#dc2626',
    fontWeight: 'bold',
    marginBottom: 10,
  },
  errorText: {
    color: '#991b1b',
  },
});
