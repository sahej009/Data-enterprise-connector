import { useState } from "react";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("dashboard");

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newMessages = [...messages, { role: "Human", content: input }];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: input,
          history: messages.map((m) => [m.role, m.content]),
        }),
      });
      const data = await response.json();
      setMessages([...newMessages, { role: "AI", content: data.reply }]);
    } catch (error) {
      console.error("Error:", error);
      setMessages([
        ...newMessages,
        { role: "AI", content: "Sorry, the server is offline." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 font-sans text-gray-800">
      {/* LEFT: Sidebar Navigation */}
      <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-6 border-b border-gray-200">
          <h1 className="text-xl font-bold text-indigo-600">Enterprise AI</h1>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <button
            onClick={() => setActiveTab("dashboard")}
            className={`w-full text-left block px-4 py-2 rounded-md font-medium transition-colors ${activeTab === "dashboard" ? "bg-indigo-50 text-indigo-700" : "text-gray-600 hover:bg-gray-100"}`}
          >
            Dashboard
          </button>
          <button
            onClick={() => setActiveTab("clients")}
            className={`w-full text-left block px-4 py-2 rounded-md font-medium transition-colors ${activeTab === "clients" ? "bg-indigo-50 text-indigo-700" : "text-gray-600 hover:bg-gray-100"}`}
          >
            Client Directory
          </button>
          <button
            onClick={() => setActiveTab("sales")}
            className={`w-full text-left block px-4 py-2 rounded-md font-medium transition-colors ${activeTab === "sales" ? "bg-indigo-50 text-indigo-700" : "text-gray-600 hover:bg-gray-100"}`}
          >
            Sales Reports
          </button>
        </nav>
      </div>

      {/* CENTER: Main Data Workspace */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white border-b border-gray-200 p-4 shadow-sm z-10 flex justify-between items-center">
          <h2 className="text-lg font-semibold">
            {activeTab === "dashboard" && "Dashboard Overview"}
            {activeTab === "clients" && "Client Directory"}
            {activeTab === "sales" && "Sales Reports"}
          </h2>
          <span className="text-sm text-gray-500">Welcome back, Admin</span>
        </header>

        <main className="flex-1 p-6 overflow-auto">
          {activeTab === "dashboard" && (
            <div className="bg-white border border-gray-200 rounded-lg p-8 shadow-sm h-full flex flex-col items-center justify-center text-center transition-all">
              <div className="bg-indigo-100 p-4 rounded-full mb-4">
                <svg
                  className="w-8 h-8 text-indigo-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  ></path>
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-2">
                Welcome to your Data Workspace
              </h3>
              <p className="text-gray-500 max-w-md">
                Use the AI Copilot on the right to query the CRM database or
                search through corporate strategy documents.
              </p>
            </div>
          )}

          {activeTab === "clients" && (
            <div className="bg-white border border-gray-200 rounded-lg p-8 shadow-sm transition-all">
              <h3 className="text-xl font-bold mb-4 border-b pb-2">
                Client Directory
              </h3>
              <p className="text-gray-500">
                Ask the AI Copilot: "Who is our top client?" to pull data into
                this view.
              </p>
              {/* Future feature: Render a Tailwind table of clients here */}
            </div>
          )}

          {activeTab === "sales" && (
            <div className="bg-white border border-gray-200 rounded-lg p-8 shadow-sm transition-all">
              <h3 className="text-xl font-bold mb-4 border-b pb-2">
                Sales Reports (Q3)
              </h3>
              <p className="text-gray-500">
                Ask the AI Copilot: "What were our total sales for Initech?" to
                see analytics.
              </p>
              {/* Future feature: Render sales charts here */}
            </div>
          )}
        </main>
      </div>

      {/* RIGHT: AI Copilot Sidebar */}
      <div className="w-96 bg-white border-l border-gray-200 flex flex-col shadow-lg z-20">
        <div className="p-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
          <h2 className="font-semibold text-gray-700 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-green-500"></span>
            AI Copilot
          </h2>
        </div>

        {/* Chat History Area */}
        <div className="flex-1 p-4 overflow-y-auto space-y-4 bg-gray-50">
          {messages.length === 0 && (
            <div className="text-center text-gray-400 text-sm mt-10">
              How can I help you analyze the data today?
            </div>
          )}

          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.role === "Human" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[85%] rounded-lg p-3 text-sm ${msg.role === "Human" ? "bg-indigo-600 text-white rounded-br-none" : "bg-white border border-gray-200 text-gray-800 rounded-bl-none shadow-sm"}`}
              >
                {msg.content}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white border border-gray-200 text-gray-500 rounded-lg rounded-bl-none p-3 text-sm shadow-sm flex gap-1 items-center">
                <span className="animate-bounce">●</span>
                <span className="animate-bounce delay-100">●</span>
                <span className="animate-bounce delay-200">●</span>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="p-4 bg-white border-t border-gray-200">
          <form onSubmit={sendMessage} className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question..."
              disabled={isLoading}
              className="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100"
            />
            <button
              type="submit"
              disabled={isLoading}
              className="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700 disabled:opacity-50 transition-colors"
            >
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;
