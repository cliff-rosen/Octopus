import React from 'react';
import { Button } from "../components/ui/button"

interface ScreenDisplayProps {
    screen: {
        id: string;
        name: string;
        content: string;
    };
    onUpdate: (id: string) => void;
    borderColor: string;
}

const ScreenDisplay: React.FC<ScreenDisplayProps> = ({ screen, onUpdate, borderColor }) => {
    return (
        <div className={`border-2 ${borderColor} rounded-lg p-4 flex flex-col bg-gray-800 shadow-md`} style={{ height: '400px' }}>
            <h3 className="text-xl font-bold mb-2 text-gray-200">{screen.name}</h3>
            <div className="flex-grow overflow-auto border border-gray-600 p-2 mb-4 bg-gray-700" style={{ height: '300px', minHeight: '300px', maxHeight: '300px' }}>
                <pre className="whitespace-pre-wrap h-full text-gray-300">{screen.content}</pre>
            </div>
            <Button onClick={() => onUpdate(screen.id)} className="bg-blue-600 hover:bg-blue-700 text-white">Update</Button>
        </div>
    );
};

export default ScreenDisplay;