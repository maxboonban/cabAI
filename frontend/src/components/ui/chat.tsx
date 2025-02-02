"use client";

import { useState, useEffect } from "react";

const Chat = () => {
    const [input, setInput] = useState("");
    const [response, setResponse] = useState("");
    const [displayedResponse, setDisplayedResponse] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        if (!input.trim()) return;

        setResponse("");
        setDisplayedResponse(""); // Clear previous responses
        setLoading(true);

        try {
            const res = await fetch("/api/chat", { // implement this
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt: input }),
            });

            const data = await res.json();
            setResponse(data.response || "No response");
        } catch (error) {
            setResponse("Error fetching response");
        }

        setLoading(false);
        setInput(""); // Clear input field
    };

    // Typewriter effect for response
    useEffect(() => {
        if (!response) return;

        let i = 0;
        setDisplayedResponse("");
        const interval = setInterval(() => {
            setDisplayedResponse((prev) => prev + response[i]);
            i++;
            if (i === response.length) clearInterval(interval);
        }, 50); // Adjust speed

        return () => clearInterval(interval);
    }, [response]);

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-obsidian text-white p-4">
            <div className="w-full max-w-2xl bg-[#162636] p-6 rounded-lg shadow-lg flex flex-col space-y-4">
                
                {/* Response Box (on top) */}
                {response && (
                    <div className="p-4 bg-obsidian rounded">
                        <strong>Response:</strong>
                        <p className="whitespace-pre-line">{displayedResponse}</p>
                    </div>
                )}

                {/* Prompt Input */}
                <textarea
                    className="w-full p-3 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:none"
                    placeholder="Type your question here..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    rows={3}
                />

                {/* Submit Button (ADD HOVER EFFECT)*/}
                <button
                    className="w-full bg-gradient-to-tr from-[#964B00] via-[#BB2525] to-[#FFD369] text-white py-2 px-4 rounded transition"
                    onClick={handleSubmit}
                    disabled={loading}
                >
                    {loading ? "Thinking..." : "Submit"}
                </button>
            </div>
        </div>
    );
};

export default Chat;
