
// ===============================
// MongoDB Final Project Script
// Database: bigdata_final_project
// ===============================

1. Database Setup & Verification

// Switch to project database
use bigdata_final_project;

// Verify collections exist
show collections;

// Document counts (proof of data loading)
db.users.countDocuments();
db.products.countDocuments();
db.categories.countDocuments();
db.transactions.countDocuments();

2. Indexes (Performance & Justification)

// Users: fast lookup by user_id
db.users.createIndex({ user_id: 1 });

// Products: category-based analytics
db.products.createIndex({ category_id: 1 });

// Transactions: common analytics dimensions
db.transactions.createIndex({ user_id: 1 });
db.transactions.createIndex({ timestamp: 1 });

3. Aggregation 1: Product Popularity (Top Selling Products)


db.transactions.aggregate([
  { $unwind: "$items" },
  {
    $group: {
      _id: "$items.product_id",
      total_quantity_sold: { $sum: "$items.quantity" },
      total_revenue: { $sum: "$items.subtotal" }
    }
  },
  { $sort: { total_quantity_sold: -1 } },
  { $limit: 10 }
]);


4. Aggregation 2: Revenue by Category


db.transactions.aggregate([
  { $unwind: "$items" },
  {
    $lookup: {
      from: "products",
      localField: "items.product_id",
      foreignField: "product_id",
      as: "product_info"
    }
  },
  { $unwind: "$product_info" },
  {
    $group: {
      _id: "$product_info.category_id",
      total_revenue: { $sum: "$items.subtotal" }
    }
  },
  { $sort: { total_revenue: -1 } }
]);


5. Aggregation 3: User Purchase Frequency (Segmentation)

db.transactions.aggregate([
  {
    $group: {
      _id: "$user_id",
      total_transactions: { $sum: 1 },
      total_spent: { $sum: "$total" }
    }
  },
  { $sort: { total_transactions: -1 } }
]);


6. Sample Document Queries (Screenshots)

db.users.findOne();
db.products.findOne();
db.transactions.findOne();

















