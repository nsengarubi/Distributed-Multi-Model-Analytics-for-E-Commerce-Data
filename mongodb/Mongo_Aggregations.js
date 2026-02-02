use ecommerce_db

// Revenue by category
db.transactions.aggregate([
  { $unwind: "$items" },
  {
    $lookup: {
      from: "products",
      localField: "items.product_id",
      foreignField: "product_id",
      as: "product"
    }
  },
  { $unwind: "$product" },
  {
    $group: {
      _id: "$product.category_id",
      total_revenue: { $sum: "$items.subtotal" }
    }
  },
  { $sort: { total_revenue: -1 } }
])

// Customer spending summary
db.transactions.aggregate([
  {
    $group: {
      _id: "$user_id",
      transaction_count: { $sum: 1 },
      total_spent: { $sum: "$total" }
    }
  },
  { $sort: { total_spent: -1 } }
])
