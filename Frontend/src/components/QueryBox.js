import React from "react";

const QueryBox = ({ onSendQuery }) => {
  const predefinedQueries = [
    "How to cancel your order?",
    "Issues with payment",
    "Want to change Email Credentials",
  ];

  return (
    <div className="query-boxes">
      {predefinedQueries.map((query, index) => (
        <div
          key={index}
          className="query-box"
          onClick={() => onSendQuery(query)}
        >
          {query}
        </div>
      ))}
    </div>
  );
};

export default QueryBox;
