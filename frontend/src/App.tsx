import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import DimensionsPage from './pages/DimensionsPage';
import SelectionPage from './pages/SelectionPage';
import GardenViewPage from './pages/GardenViewPage';
import AdminPage from './pages/AdminPage';

function Nav() {
  const { pathname } = useLocation();
  const links = [
    { to: '/', label: 'Dimensions' },
    { to: '/selection', label: 'Selection' },
    { to: '/garden', label: 'Potager' },
    { to: '/admin', label: 'Admin' },
  ];

  return (
    <nav className="bg-green-800 text-white">
      <div className="max-w-5xl mx-auto px-4 flex items-center h-12 gap-6">
        <span className="font-bold text-lg mr-4">GardenGen</span>
        {links.map((l) => (
          <Link
            key={l.to}
            to={l.to}
            className={`text-sm transition-colors ${
              pathname === l.to ? 'text-white font-medium' : 'text-green-200 hover:text-white'
            }`}
          >
            {l.label}
          </Link>
        ))}
      </div>
    </nav>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Nav />
      <Routes>
        <Route path="/" element={<DimensionsPage />} />
        <Route path="/selection" element={<SelectionPage />} />
        <Route path="/garden" element={<GardenViewPage />} />
        <Route path="/admin" element={<AdminPage />} />
      </Routes>
    </BrowserRouter>
  );
}
