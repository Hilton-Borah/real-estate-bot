import { useState, useRef, useEffect } from 'react';
import { PaperAirplaneIcon, BuildingOfficeIcon } from '@heroicons/react/24/solid';
import ChatMessage from './ChatMessage';
import DataVisualization from './DataVisualization';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (messages.length > 0) {
      scrollToBottom();
    }
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = {
      type: 'user',
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/analyze/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: input }),
      });

      const data = await response.json();

      const botMessage = {
        type: 'bot',
        content: data.summary,
        chartData: data.chart_data,
        tableData: data.table_data,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        type: 'bot',
        content: 'Sorry, I encountered an error while processing your request.',
      };
      setMessages((prev) => [...prev, errorMessage]);
    }

    setLoading(false);
  };

  const exampleQueries = [
    {
      text: "Analyze property trends in Wakad",
      icon: "🏘️",
      description: "Get market insights"
    },
    {
      text: "Compare prices in Aundh and Baner",
      icon: "📊",
      description: "Area comparison"
    },
    {
      text: "Show rental trends in Kothrud",
      icon: "📈",
      description: "Rental analysis"
    }
  ];

  return (
    <div className="chat-container" style={{width:"1520px"}}>
      <div className="w-full mx-auto">
        {/* Header */}
        <div className="card mb-6 bg-gradient-to-r from-blue-600 to-blue-700 text-white">
          <div className="flex items-center gap-3 mb-4">
            <BuildingOfficeIcon className="w-8 h-8" />
            <h1 className="text-2xl font-bold">Real Estate Assistant</h1>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-6">
            {exampleQueries.map((query, index) => (
              <button
                key={index}
                className="bg-white/10 hover:bg-white/20 rounded-lg p-3 text-left transition-all"
                onClick={() => setInput(query.text)}
              >
                <span className="text-xl mb-2 block">{query.icon}</span>
                <p className="text-sm font-medium">{query.text}</p>
                <p className="text-xs text-blue-200 mt-1">{query.description}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Messages */}
        <div className="card mb-6 min-h-[400px] max-h-[600px] overflow-y-auto">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-gray-500 p-4 text-center">
              <BuildingOfficeIcon className="w-12 h-12 mb-4 text-gray-400" />
              <p className="text-lg font-medium">Welcome! How can I help you?</p>
              <p className="text-sm mt-2">Try one of the example queries above to get started</p>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message, index) => (
                <ChatMessage key={index} message={message} />
              ))}
              {loading && (
                <div className="flex justify-center">
                  <div className="loading-dots">
                    <div className="loading-dot" />
                    <div className="loading-dot" />
                    <div className="loading-dot" />
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input */}
        <div className="card">
          <form onSubmit={handleSubmit} className="flex gap-3 text-white">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about real estate trends..."
              className="input-field"
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="btn-primary"
            >
              <PaperAirplaneIcon className="h-5 w-5" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface; 