import { useState } from 'react';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");

    const res = await fetch("http://localhost:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input })
    });

    const data = await res.json();
    const botMsg = { role: "ai", content: data.reply };
    setMessages(prev => [...prev, botMsg]);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-xl bg-white shadow-md rounded-lg p-4">
        <h1 className="text-xl font-bold mb-4">AI Chatbot</h1>
        <div className="h-64 overflow-y-auto border rounded p-2 mb-4">
          {messages.map((msg, idx) => (
            <div key={idx} className={`mb-2 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
              <span className={`inline-block px-3 py-1 rounded-lg ${msg.role === 'user' ? 'bg-blue-200' : 'bg-gray-200'}`}>
                {msg.content}
              </span>
            </div>
          ))}
        </div>
        <div className="flex gap-2">
          <input
            className="flex-1 border rounded p-2"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          />
          <button className="bg-blue-500 text-white px-4 py-2 rounded" onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
