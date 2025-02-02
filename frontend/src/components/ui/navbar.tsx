import Link from 'next/link';
import Button from './button'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRightToBracket } from '@fortawesome/free-solid-svg-icons';

const Navbar = () => {
    return (
        <div className='bg-obsidian w-full p-4'>
            <nav className="border border-[#26292f] rounded-lg h-20 flex justify-between items-center my-2 mx-10 px-6">
                <Link href="/" className="font-bold text-2xl text-transparent bg-clip-text bg-gradient-to-tr from-[#964B00] via-[#BB2525] to-[#FFD369]">
                    C@B AI
                </Link>
                <div className="gradient-border p-4">
                    <Button variant="primary" size="sm" className="rounded-lg">
                        <FontAwesomeIcon icon={faRightToBracket} className="mr-2 w-4 h-4" />
                        Sign in
                    </Button>
                </div>
            </nav>
        </div>
    );
};

export default Navbar;
