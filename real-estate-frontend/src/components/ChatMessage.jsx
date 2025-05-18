import { UserIcon, BuildingOfficeIcon } from '@heroicons/react/24/solid';
import DataVisualization from './DataVisualization';

const ChatMessage = ({ message }) => {
  const isUser = message.type === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center mr-3">
          <BuildingOfficeIcon className="w-5 h-5 text-white" />
        </div>
      )}
      
      <div className="space-y-3">
        <div className={`message-bubble ${isUser ? 'message-bubble-user' : 'message-bubble-bot'}`}>
          <p className="text-sm">{message.content}</p>
        </div>

        {!isUser && message.chartData && (
          <div className="mt-4 bg-white rounded-lg p-4 shadow-sm">
            <DataVisualization
              chartData={message.chartData}
              tableData={message.tableData}
            />
          </div>
        )}
      </div>

      {isUser && (
        <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center ml-3">
          <UserIcon className="w-5 h-5 text-white" />
        </div>
      )}
    </div>
  );
};

export default ChatMessage; 