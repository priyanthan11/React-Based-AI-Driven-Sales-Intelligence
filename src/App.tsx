// import { useEffect, useState } from "react";
// import "./DealsTable.css";
// interface Deal {
//   opportunity_id: string;
//   sales_agent: string;
//   product: string;
//   account: string;
//   deal_stage: string;
//   close_value: number;
//   win_probability?: number; // if you also return model predictions
// }

// export default function DealsTable() {
//   const [deals, setDeals] = useState<Deal[]>([]);

//   useEffect(() => {
//     fetch("http://localhost:8000/deals") // your FastAPI server
//       .then((res) => res.json())
//       .then((data) => setDeals(data));
//   }, []);

//   return (
//     <table>
//       <thead>
//         <tr>
//           <th>ID</th>
//           <th>Agent</th>
//           <th>Product</th>
//           <th>Stage</th>
//           <th>Value</th>
//         </tr>
//       </thead>
//       <tbody>
//         {deals.map((deal) => (
//           <tr key={deal.opportunity_id}>
//             <td data-label="ID">{deal.opportunity_id}</td>
//             <td data-label="Agent">{deal.sales_agent}</td>
//             <td data-label="Product">{deal.product}</td>
//             <td data-label="Stage">{deal.deal_stage}</td>
//             <td data-label="Value">{deal.close_value}</td>
//           </tr>
//         ))}
//       </tbody>
//     </table>
//   );
// }
// App.tsx
import React, { useState, useEffect } from "react";
import DealsTable from "./fronted/src/components/DealsTable.jsx";

interface Deal {
  opportunity_id: string;
  sales_agent: string;
  product: string;
  account: string;
  engage_date: string;
  close_date: string;
  close_value: number;
}

// Demo data for testing UI
const demoDeals: Deal[] = [
  {
    opportunity_id: "1",
    sales_agent: "Alice",
    product: "GTX Basic",
    account: "Acme Corp",
    engage_date: "2025-09-01",
    close_date: "2025-09-30",
    close_value: 50000,
  },
  {
    opportunity_id: "2",
    sales_agent: "Bob",
    product: "MG Special",
    account: "Beta Ltd",
    engage_date: "2025-09-05",
    close_date: "2025-10-05",
    close_value: 75000,
  },
  {
    opportunity_id: "3",
    sales_agent: "Charlie",
    product: "Hottechi",
    account: "Gamma Inc",
    engage_date: "2025-09-10",
    close_date: "2025-10-10",
    close_value: 120000,
  },
];

function App() {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [predictions, setPredictions] = useState<{
    [key: string]: { win_probability: number };
  }>({});

  useEffect(() => {
    // Load demo deals
    setDeals(demoDeals);

    // Simulate predictions (random win probability) for demo
    const fakePreds: { [key: string]: { win_probability: number } } = {};
    demoDeals.forEach((d) => {
      fakePreds[d.opportunity_id] = { win_probability: Math.random() };
    });
    setPredictions(fakePreds);
  }, []);

  return (
    <div className="p-8 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Sales Deals Dashboard</h1>
      <DealsTable deals={deals} predictions={predictions} />
    </div>
  );
}

export default App;
