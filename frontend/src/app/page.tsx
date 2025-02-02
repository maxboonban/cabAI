import Navbar from "@/components/ui/navbar";
import Hero from "@/components/ui/hero";
import Chat from "@/components/ui/chat";
import Box from "@/components/ui/card";

const Home = () => {
  return (
    <>
      <Navbar/>
      <main>
        <Hero />
        <Chat />
      </main>
    </>
  );
};

export default Home;
