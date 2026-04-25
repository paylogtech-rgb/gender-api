# Stage 2 Backend – Intelligence Query Engine

## Overview
This project implements a demographic intelligence API for Insighta Labs. It allows clients to query profile data using advanced filtering, sorting, pagination, and natural language search.

---

## Features Implemented

### 1. Filtering
The `/api/profiles` endpoint supports filtering by:
- gender
- age_group
- country_id
- min_age, max_age
- min_gender_probability
- min_country_probability

All filters can be combined in a single request.

---

### 2. Sorting
Clients can sort results using:
- age
- created_at
- gender_probability

Order:
- asc
- desc

---

### 3. Pagination
Pagination is implemented using:
- page (default: 1)
- limit (default: 10, max: 50)

The response includes:
- page
- limit
- total records

---

---

## 🧠 Parsing Approach

The natural language search is implemented using a **rule-based parser**.

The system:
1. Converts the query to lowercase
2. Checks for specific keywords
3. Maps keywords to database filters
4. Applies filters using Django ORM

Example:
- "young males from nigeria"
  → gender=male
  → age between 16–24
  → country_id=NG

---

## 🔑 Supported Keywords

### Gender
- "male"
- "female"

### Age Keywords
- "young" → 16–24
- "adult"
- "teenager"

### Age Conditions
- "above <number>"

### Countries
- "nigeria" → NG
- "kenya" → KE
- "angola" → AO

---

## ⚠️ Limitations

- Only predefined keywords are supported
- Does not handle complex sentences
- Cannot interpret multiple numeric conditions (e.g., "between 20 and 30")
- Limited country support (only mapped ones)
- No typo handling (e.g., "nigerai" will fail)

---

## Tech Stack
- Django
- Django REST Framework
- SQLite (development)

---

## Notes
- Rule-based parsing only (no AI/LLM used)
- UUID v7 used for primary keys
- CORS enabled for external access
### 4. Natural Language Search

Endpoint:
