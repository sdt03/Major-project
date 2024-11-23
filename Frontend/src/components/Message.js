import React from "react";

const Message = ({ sender, text }) => (
  <div className={`chat-message ${sender === "user" ? "user-message" : "system-message"}`}>
    {text}
  </div>
);

export default Message;
