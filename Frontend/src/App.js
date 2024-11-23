// // // App.js
// // import React, { useState } from "react";
// // import "./App.css";

// // const App = () => {
// //   const [userQuery, setUserQuery] = useState("");
// //   const [chatMessages, setChatMessages] = useState([]);
// //   const [isRecording, setIsRecording] = useState(false);

// //   const handleBoxClick = (query) => {
// //     setChatMessages((prev) => [...prev, { sender: "user", text: query }]);
// //     setChatMessages((prev) => [...prev, { sender: "system", text: "Loading..." }]);
// //   };

// //   const handleSendClick = () => {
// //     if (userQuery.trim()) {
// //       setChatMessages((prev) => [...prev, { sender: "user", text: userQuery }]);
// //       setChatMessages((prev) => [...prev, { sender: "system", text: "Loading..." }]);
// //       setUserQuery(""); // Clear input
// //     }
// //   };

// //   const handleMicClick = () => {
// //     // Placeholder: Simulate starting/stopping recording
// //     setIsRecording((prev) => !prev);
// //   };

// //   return (
// //     <div className="App">
// //       <header className="App-header">
// //         Welcome to SupportGPT from Haldi.AI
// //       </header>
// //       <main>
// //         <div className="query-boxes">
// //           {["How to cancel your order?", "Issue's with payment", "Want to change Email Credentials"].map(
// //             (query, index) => (
// //               <div
// //                 key={index}
// //                 className="query-box"
// //                 onClick={() => handleBoxClick(query)}
// //               >
// //                 {query}
// //               </div>
// //             )
// //           )}
// //         </div>
// //         <div className="chat-section">
// //           <div className="chat-window">
// //             {chatMessages.map((message, index) => (
// //               <div
// //                 key={index}
// //                 className={`chat-message ${
// //                   message.sender === "user" ? "user-message" : "system-message"
// //                 }`}
// //               >
// //                 {message.text}
// //               </div>
// //             ))}
// //           </div>
// //           <div className="input-section">
// //             <textarea
// //               value={userQuery}
// //               onChange={(e) => setUserQuery(e.target.value)}
// //               placeholder="Ask your Query..."
// //               maxLength="1000"
// //             />
// //             <button onClick={handleSendClick} className="send-button">
// //               <span>&uarr;</span>
// //             </button>
// //             <button onClick={handleMicClick} className="mic-button">
// //               <span role="img" aria-label="mic">
// //                 🎤
// //               </span>
// //             </button>
// //           </div>
// //         </div>
// //       </main>
// //     </div>
// //   );
// // };

// // export default App;

import React, { useState } from "react";
import "./App.css";
import Header from "./components/Header";
import QueryBoxes from "./components/QueryBox";
import ChatBox from "./components/ChatBox";

const App = () => {
  const [chatMessages, setChatMessages] = useState([]);

  const handleSendQuery = async (query) => {
    if (query.trim()) {
      setChatMessages((prev) => [...prev, { sender: "user", text: query }]);
      try {
        const response = await fetch("http://localhost:5001/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: query }),
          mode: "cors",
        });

        if (!response.ok) throw new Error(`Server Error: ${response.status}`);

        const data = await response.json();
        setChatMessages((prev) => [
          ...prev,
          { sender: "system", text: data.answer || "No response received." },
        ]);
      } catch (error) {
        setChatMessages((prev) => [
          ...prev,
          { sender: "system", text: `Error: ${error.message}` },
        ]);
      }
    }
  };

  return (
    <div className="App">
      <Header title="Welcome to SupportGPT" />
      <QueryBoxes onSendQuery={handleSendQuery} />
      <ChatBox chatMessages={chatMessages} onSendQuery={handleSendQuery} />
    </div>
  );
};

export default App;
