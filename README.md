# Distributed Multi-Model Analytics for E-Commerce Data

## Big Data Analytics – Final Project

This project implements a **distributed multi-model analytics system** for a synthetic e-commerce dataset using **MongoDB**, **HBase**, and **Apache Spark**.  
Each technology is selected based on its strengths in handling different data characteristics, and Apache Spark is used as the unified analytics and integration engine.


##  Project Objectives

- Design appropriate data models for **MongoDB** and **HBase**
- Perform large-scale data processing using **Apache Spark**
- Integrate heterogeneous data sources for advanced analytics
- Generate business insights through **visualization**
- Demonstrate scalability, integration, and analytical reasoning


##  System Architecture Overview

The system follows a layered architecture:

1. **Storage Layer**
   - **MongoDB**: User profiles, products, and transactions (document-oriented data)
   - **HBase**: User session activity (time-series, wide-column data)

2. **Processing Layer**
   - **Apache Spark**: Data cleaning, normalization, aggregation, and cross-system analytics

3. **Presentation Layer**
   - **Python (Matplotlib)**: Static visualizations for business insights


##  Repository Structure

Big_Data_Analytics_Final_Project/
│
├── data/
│ ├── users.json
│ ├── products.json
│ ├── categories.json
│ ├── transactions.json
│ └── sessions_0.json
│
├── spark/
│ ├── Part2_Spark_Processing.ipynb
│ ├── Part3_Analytics_Integration.ipynb
│ └── Spark_SQL_Queries.sql
│
├── mongodb/
│ ├── MongoDB_Schemas_and_Load_Commands.js
│ └── Mongo_Aggregations.js
│
├── hbase/
│ └── HBase_Commands.txt
│
├── report/
│ ├── Big_Data_Analytics_Final_Project_Report.pdf
│ └── figures/
│
├── README.md
└── requirements.txt


##  Data Modeling

### MongoDB
- Collections: `users`, `products`, `transactions`
- Stores nested and semi-structured data (e.g., transaction items)
- Supports aggregation pipelines for analytics

### HBase
- Table: `ecommerce:user_sessions`
- Row key: `user_id_timestamp`
- Column families: `session`, `metrics`, `device`, `geo`
- Optimized for time-series and sparse data



##  Data Processing with Apache Spark (Part 2)

Spark is used to:
- Load multi-line JSON data
- Clean and normalize datasets
- Explode nested transaction items
- Join datasets and compute revenue analytics

Key outputs:
- Cleaned transactions dataset
- Revenue by product category
- Product interaction analysis



##  Analytics Integration (Part 3)

### Use Case: Customer Lifetime Value (CLV)

**Business Question:**  
Which customers generate the highest long-term value based on purchase behavior and engagement?

**Integrated Data Sources:**
- Transactions (MongoDB)
- Session engagement (HBase)

**Processing:**
- Aggregate transaction totals per user
- Aggregate session counts and durations per user
- Join datasets using Spark
- Compute a composite CLV score



##  Visualization & Insights (Part 4)

Static visualizations were generated using Python to communicate analytical findings:

- Revenue by product category
- Top customers by lifetime value
- Transaction frequency distribution
- User session engagement distribution

These visualizations support data-driven business insights.



##  Scalability Considerations

- **MongoDB** supports sharding for horizontal scalability
- **HBase** scales across distributed clusters for large session datasets
- **Apache Spark** enables parallel and distributed analytics
- Architecture can be extended to real-time analytics using Spark Streaming


##  Limitations

- Dataset is synthetic
- Limited transaction volume affects visual diversity
- Real-world datasets would provide richer analytical patterns



##  Future Work

- Real-time analytics and streaming ingestion
- Recommendation systems
- Interactive dashboards
- Machine learning–based customer segmentation


##  Requirements

- Python 3.x
- Apache Spark
- MongoDB
- HBase
- Python libraries: `pyspark`, `matplotlib`, `pandas`


##  How Reproduced Results

1. Load datasets into MongoDB and HBase using scripts in `/mongodb` and `/hbase`
2. Run Spark notebooks in `/spark` in order:
   - Part2_Spark_Processing.ipynb
   - Part3_Analytics_Integration.ipynb
3. Generate visualizations and export results
4. Review findings in the final report


##  Report

The final technical report is available in:

report/Big_Data_Analytics_Final_Project_Report.pdf