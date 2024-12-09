import './App.css';
import { Outlet } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';

function App() {
  return (
    <>
    <div className="d-flex flex-column justify-content-between gap-4">
    <Header />
    <div className="me-5 ms-5">
        <Outlet />
    </div>
    <Footer />
    </div>
    </>
  );
}

export default App;
