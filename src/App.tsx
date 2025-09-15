import { useEffect, useState } from "react";
import "./DealsTable.css";
interface Deal {
  opportunity_id: string;
  sales_agent: string;
  product: string;
  account: string;
  deal_stage: string;
  close_value: number;
  win_probability?: number; // if you also return model predictions
}

export default function DealsTable() {
  const [deals, setDeals] = useState<Deal[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/deals") // your FastAPI server
      .then((res) => res.json())
      .then((data) => setDeals(data));
  }, []);

  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Agent</th>
          <th>Product</th>
          <th>Stage</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        {deals.map((deal) => (
          <tr key={deal.opportunity_id}>
            <td data-label="ID">{deal.opportunity_id}</td>
            <td data-label="Agent">{deal.sales_agent}</td>
            <td data-label="Product">{deal.product}</td>
            <td data-label="Stage">{deal.deal_stage}</td>
            <td data-label="Value">{deal.close_value}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
