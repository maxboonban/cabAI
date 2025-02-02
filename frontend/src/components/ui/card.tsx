// Box.tsx

interface BoxProps {
    title: string;
    description: string;
    image: string;
}

const Card: React.FC<BoxProps> = ({ title, description, image }) => {
    return (
        <div className="bg-white p-6 rounded-lg shadow-lg text-center flex flex-col items-center">
            <img src={image} alt={title} className="w-full h-auto rounded-md mb-4" />
            <h3 className="text-xl font-semibold text-gray-800 mb-2">{title}</h3>
            <p className="text-gray-600">{description}</p>
        </div>
    );
};

export default Card;

