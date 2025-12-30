#!/bin/bash

# GetLanded API Demo Script
# This demonstrates the complete career intelligence flow

echo "=== GetLanded Career Intelligence API Demo ==="
echo ""

# Health check
echo "1. Health Check:"
curl -s http://localhost:8000/health | jq
echo ""

# Create a student
echo "2. Creating Student (Alice Johnson):"
STUDENT=$(curl -s -X POST "http://localhost:8000/students" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "university": "University of Example",
    "graduation_year": 2025
  }')

STUDENT_ID=$(echo $STUDENT | jq -r '.id')
echo "Created student with ID: $STUDENT_ID"
echo $STUDENT | jq
echo ""

# Submit psychometric assessment
echo "3. Submitting Psychometric Assessment:"
PSYCH_PROFILE=$(curl -s -X POST "http://localhost:8000/students/$STUDENT_ID/psychometrics" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": {
      "Q1": 5, "Q2": 2, "Q3": 4, "Q4": 5,
      "Q5": 4, "Q6": 2, "Q7": 5, "Q8": 4,
      "Q9": 3, "Q10": 3, "Q11": 5, "Q12": 2
    }
  }')

echo "Psychometric Profile Generated:"
echo $PSYCH_PROFILE | jq
echo ""

# Get career matches (this will fail without student skills, so let's just show top 3)
echo "4. Getting Top 3 Career Matches:"
curl -s "http://localhost:8000/role-clusters?tenant_id=1" | jq '.[0:3] | .[] | {name, description, example_careers}'
echo ""

echo "=== Demo Complete ==="
echo ""
echo "Access the full API documentation at: http://localhost:8000/docs"
echo ""
