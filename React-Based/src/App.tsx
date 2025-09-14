import { useEffect, useState } from "react";

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
            <td>{deal.opportunity_id}</td>
            <td>{deal.sales_agent}</td>
            <td>{deal.product}</td>
            <td>{deal.deal_stage}</td>
            <td>{deal.close_value}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
