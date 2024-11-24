import React, { useState } from "react";
import Message from "./Message";

const ChatBox = ({ 
  chatMessages, 
  onSendQuery, 
  onStartMic, 
  onStopMic, 
  isListening, 
  userInput, 
  setUserInput, }) => {

  const handleSend = () => {
    if (userInput.trim()) {
      onSendQuery(userInput);
      setUserInput("");
    }
  };

  return (
    <div className="chat-section">
      <div className="chat-window">
        {chatMessages.map((message, index) => (
          <Message
            key={index}
            sender={message.sender}
            text={message.text}
          />
        ))}
      </div>
      <div className="input-section">
        <div className="textarea-container">
        <textarea
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button onClick={handleSend} className="send-button">Send</button>
        <button
            onClick={isListening ? onStopMic : onStartMic}
            className={`mic-btn ${isListening ? "active" : ""}`} // Optional: Add active state styles
          >
            {isListening ? "Stop" : "Mic"}
          </button>
        
        </div>
      </div>
    </div>
  );
};

export default ChatBox;
