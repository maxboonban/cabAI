import React from 'react';
import Button from './button';

const Hero: React.FC = () => {
    return (
        <section className="bg-obsidian" style={{ height: 'calc(100vh - 80px)' }}> {/* Assuming navbar height is 80px */}
            <div className="container mx-auto text-center text-white pt-20">
                <h1 className="text-6xl font-bold mb-8">Welcome to Courses @ Brown AI</h1>
                <p className="text-xl mb-8 text-[#9ca3af]">Your Personalized Path to Success: AI Course Recommendations at Brown</p>
                <button className="bg-gradient-to-tr from-[#964B00] via-[#BB2525] to-[#FFD369] text-white py-3 px-10 rounded">
                    Get Started
                </button>
            </div>
        </section>
    );
};

export default Hero;
