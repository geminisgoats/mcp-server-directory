import React, { useState, useEffect } from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Main Homepage Component
const Homepage = () => {
  const [featuredServers, setFeaturedServers] = useState([]);
  const [sponsoredServers, setSponsoredServers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFeaturedServers();
    fetchSponsoredServers();
  }, []);

  const fetchFeaturedServers = async () => {
    try {
      const response = await axios.get(`${API}/featured-servers`);
      setFeaturedServers(response.data);
    } catch (error) {
      console.error('Error fetching featured servers:', error);
    }
  };

  const fetchSponsoredServers = async () => {
    try {
      const response = await axios.get(`${API}/sponsored-servers`);
      setSponsoredServers(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching sponsored servers:', error);
      setLoading(false);
    }
  };

  const trackClick = async (serverId, clickType) => {
    try {
      await axios.post(`${API}/track-click`, {
        server_id: serverId,
        user_ip: '127.0.0.1',
        user_agent: navigator.userAgent,
        click_type: clickType
      });
    } catch (error) {
      console.error('Error tracking click:', error);
    }
  };

  const handleAffiliateClick = (server) => {
    trackClick(server.id, 'affiliate');
    window.open(server.affiliate_url, '_blank');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">MCP Directory</h1>
              <span className="ml-2 text-sm text-gray-600">Marketing & SEO</span>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={() => window.location.href = '/directory'}
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
              >
                Browse All
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Discover Top MCP Servers
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-blue-100">
              Supercharge your marketing and SEO with AI-powered MCP servers
            </p>
            <div className="flex justify-center space-x-4">
              <button
                onClick={() => window.location.href = '/directory'}
                className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                Explore Directory
              </button>
              <button
                onClick={() => window.location.href = '/directory?category=SEO Analytics'}
                className="border border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors"
              >
                SEO Tools
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Sponsored Servers Section */}
      {sponsoredServers.length > 0 && (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 py-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-2">Sponsored Servers</h2>
              <p className="text-gray-600">Premium MCP servers recommended by our partners</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {sponsoredServers.map((server) => (
                <div key={server.id} className="bg-white rounded-lg shadow-md p-6 border-2 border-yellow-200">
                  <div className="flex items-center mb-4">
                    <img
                      src={server.logo_url}
                      alt={server.name}
                      className="w-12 h-12 rounded-lg object-cover mr-4"
                    />
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{server.name}</h3>
                      <span className="inline-block bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded">
                        Sponsored
                      </span>
                    </div>
                  </div>
                  <p className="text-gray-600 mb-4">{server.description}</p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <span className="text-yellow-500">⭐</span>
                      <span className="text-sm text-gray-600 ml-1">{server.rating}</span>
                    </div>
                    <button
                      onClick={() => handleAffiliateClick(server)}
                      className="bg-yellow-500 text-white px-4 py-2 rounded-md hover:bg-yellow-600 transition-colors"
                    >
                      Try Now
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Featured Servers Section */}
      <div className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Featured MCP Servers</h2>
            <p className="text-gray-600 text-lg">
              Handpicked servers that deliver exceptional results for marketing and SEO
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {featuredServers.map((server) => (
              <div key={server.id} className="bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow p-6">
                <div className="flex items-center mb-4">
                  <img
                    src={server.logo_url}
                    alt={server.name}
                    className="w-16 h-16 rounded-lg object-cover mr-4"
                  />
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900">{server.name}</h3>
                    <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                      {server.category}
                    </span>
                  </div>
                </div>
                <p className="text-gray-600 mb-4">{server.description}</p>
                <div className="mb-4">
                  <div className="flex items-center mb-2">
                    <span className="text-yellow-500">⭐</span>
                    <span className="text-sm text-gray-600 ml-1">
                      {server.rating} ({server.total_reviews} reviews)
                    </span>
                  </div>
                  <div className="text-sm text-gray-600">
                    <span className="font-semibold">{server.pricing_model}</span> • {server.pricing_details}
                  </div>
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleAffiliateClick(server)}
                    className="flex-1 bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition-colors"
                  >
                    Get Started
                  </button>
                  <button
                    onClick={() => {
                      trackClick(server.id, 'details');
                      window.location.href = `/server/${server.id}`;
                    }}
                    className="flex-1 border border-gray-300 text-gray-700 py-2 rounded-md hover:bg-gray-50 transition-colors"
                  >
                    Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Categories Section */}
      <div className="bg-gray-100 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Browse by Category</h2>
            <p className="text-gray-600 text-lg">Find the perfect MCP server for your specific needs</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { name: 'SEO Analytics', icon: '📈', description: 'Optimize your search rankings' },
              { name: 'Content Generation', icon: '✍️', description: 'AI-powered content creation' },
              { name: 'Social Media Management', icon: '📱', description: 'Automate social presence' },
              { name: 'Email Marketing', icon: '📧', description: 'Engage your audience' },
              { name: 'Performance Tracking', icon: '📊', description: 'Measure your success' },
              { name: 'Keyword Research', icon: '🔍', description: 'Find profitable keywords' },
              { name: 'Competitor Analysis', icon: '🎯', description: 'Stay ahead of competition' },
              { name: 'Marketing Automation', icon: '🤖', description: 'Streamline your workflows' }
            ].map((category) => (
              <div
                key={category.name}
                onClick={() => window.location.href = `/directory?category=${encodeURIComponent(category.name)}`}
                className="bg-white rounded-lg p-6 text-center hover:shadow-md transition-shadow cursor-pointer"
              >
                <div className="text-3xl mb-3">{category.icon}</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{category.name}</h3>
                <p className="text-gray-600 text-sm">{category.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-lg font-semibold mb-4">MCP Directory</h3>
              <p className="text-gray-400">
                Discover the best MCP servers for marketing and SEO automation.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Categories</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="/directory?category=SEO Analytics" className="hover:text-white">SEO Analytics</a></li>
                <li><a href="/directory?category=Content Generation" className="hover:text-white">Content Generation</a></li>
                <li><a href="/directory?category=Social Media Management" className="hover:text-white">Social Media</a></li>
                <li><a href="/directory?category=Email Marketing" className="hover:text-white">Email Marketing</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Resources</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="/directory" className="hover:text-white">Browse All</a></li>
                <li><a href="/directory?featured=true" className="hover:text-white">Featured</a></li>
                <li><a href="/directory?pricing=Free" className="hover:text-white">Free Tools</a></li>
                <li><a href="/directory?pricing=Enterprise" className="hover:text-white">Enterprise</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Contact</h4>
              <p className="text-gray-400">
                Questions about MCP servers? Get in touch with our team.
              </p>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 MCP Directory. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

// Directory/Browse Page Component
const DirectoryPage = () => {
  const [servers, setServers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    category: '',
    pricing_model: '',
    search: ''
  });

  useEffect(() => {
    fetchServers();
  }, [filters]);

  const fetchServers = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.category) params.append('category', filters.category);
      if (filters.pricing_model) params.append('pricing_model', filters.pricing_model);
      if (filters.search) params.append('search', filters.search);

      const response = await axios.get(`${API}/servers?${params}`);
      setServers(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching servers:', error);
      setLoading(false);
    }
  };

  const trackClick = async (serverId, clickType) => {
    try {
      await axios.post(`${API}/track-click`, {
        server_id: serverId,
        user_ip: '127.0.0.1',
        user_agent: navigator.userAgent,
        click_type: clickType
      });
    } catch (error) {
      console.error('Error tracking click:', error);
    }
  };

  const handleAffiliateClick = (server) => {
    trackClick(server.id, 'affiliate');
    window.open(server.affiliate_url, '_blank');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <button
                onClick={() => window.location.href = '/'}
                className="text-2xl font-bold text-gray-900 hover:text-blue-600"
              >
                MCP Directory
              </button>
              <span className="ml-2 text-sm text-gray-600">Marketing & SEO</span>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={() => window.location.href = '/'}
                className="text-gray-600 hover:text-gray-900"
              >
                Home
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">MCP Server Directory</h1>
          
          {/* Filters */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <input
              type="text"
              placeholder="Search servers..."
              value={filters.search}
              onChange={(e) => setFilters({...filters, search: e.target.value})}
              className="px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <select
              value={filters.category}
              onChange={(e) => setFilters({...filters, category: e.target.value})}
              className="px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">All Categories</option>
              <option value="SEO Analytics">SEO Analytics</option>
              <option value="Content Generation">Content Generation</option>
              <option value="Social Media Management">Social Media Management</option>
              <option value="Email Marketing">Email Marketing</option>
              <option value="Performance Tracking">Performance Tracking</option>
              <option value="Keyword Research">Keyword Research</option>
              <option value="Competitor Analysis">Competitor Analysis</option>
              <option value="Marketing Automation">Marketing Automation</option>
            </select>
            <select
              value={filters.pricing_model}
              onChange={(e) => setFilters({...filters, pricing_model: e.target.value})}
              className="px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">All Pricing</option>
              <option value="Free">Free</option>
              <option value="Freemium">Freemium</option>
              <option value="Paid">Paid</option>
              <option value="Enterprise">Enterprise</option>
            </select>
          </div>

          <p className="text-gray-600">Found {servers.length} MCP servers</p>
        </div>

        {/* Server Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {servers.map((server) => (
            <div key={server.id} className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6">
              <div className="flex items-center mb-4">
                <img
                  src={server.logo_url}
                  alt={server.name}
                  className="w-12 h-12 rounded-lg object-cover mr-4"
                />
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{server.name}</h3>
                  <div className="flex items-center space-x-2">
                    <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                      {server.category}
                    </span>
                    {server.is_sponsored && (
                      <span className="inline-block bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded">
                        Sponsored
                      </span>
                    )}
                  </div>
                </div>
              </div>
              <p className="text-gray-600 mb-4">{server.description}</p>
              <div className="mb-4">
                <div className="flex items-center mb-2">
                  <span className="text-yellow-500">⭐</span>
                  <span className="text-sm text-gray-600 ml-1">
                    {server.rating} ({server.total_reviews} reviews)
                  </span>
                </div>
                <div className="text-sm text-gray-600">
                  <span className="font-semibold">{server.pricing_model}</span>
                </div>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => handleAffiliateClick(server)}
                  className="flex-1 bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition-colors"
                >
                  Get Started
                </button>
                <button
                  onClick={() => {
                    trackClick(server.id, 'details');
                    window.location.href = `/server/${server.id}`;
                  }}
                  className="flex-1 border border-gray-300 text-gray-700 py-2 rounded-md hover:bg-gray-50 transition-colors"
                >
                  Details
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Server Detail Page Component
const ServerDetailPage = ({ serverId }) => {
  const [server, setServer] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchServer();
  }, [serverId]);

  const fetchServer = async () => {
    try {
      const response = await axios.get(`${API}/servers/${serverId}`);
      setServer(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching server:', error);
      setLoading(false);
    }
  };

  const trackClick = async (serverId, clickType) => {
    try {
      await axios.post(`${API}/track-click`, {
        server_id: serverId,
        user_ip: '127.0.0.1',
        user_agent: navigator.userAgent,
        click_type: clickType
      });
    } catch (error) {
      console.error('Error tracking click:', error);
    }
  };

  const handleAffiliateClick = (server) => {
    trackClick(server.id, 'affiliate');
    window.open(server.affiliate_url, '_blank');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!server) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Server Not Found</h1>
          <button
            onClick={() => window.location.href = '/directory'}
            className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700"
          >
            Back to Directory
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <button
                onClick={() => window.location.href = '/'}
                className="text-2xl font-bold text-gray-900 hover:text-blue-600"
              >
                MCP Directory
              </button>
              <span className="ml-2 text-sm text-gray-600">Marketing & SEO</span>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={() => window.location.href = '/directory'}
                className="text-gray-600 hover:text-gray-900"
              >
                Directory
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="p-8">
            <div className="flex items-center mb-6">
              <img
                src={server.logo_url}
                alt={server.name}
                className="w-20 h-20 rounded-lg object-cover mr-6"
              />
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">{server.name}</h1>
                <div className="flex items-center space-x-3">
                  <span className="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                    {server.category}
                  </span>
                  {server.is_sponsored && (
                    <span className="inline-block bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm">
                      Sponsored
                    </span>
                  )}
                  {server.is_featured && (
                    <span className="inline-block bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                      Featured
                    </span>
                  )}
                </div>
              </div>
            </div>

            <p className="text-gray-600 text-lg mb-6">{server.description}</p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Features</h3>
                <ul className="space-y-2">
                  {server.features.map((feature, index) => (
                    <li key={index} className="flex items-center">
                      <span className="text-green-500 mr-2">✓</span>
                      <span className="text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Pricing</h3>
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <span className="text-2xl font-bold text-gray-900">{server.pricing_model}</span>
                  </div>
                  <p className="text-gray-600">{server.pricing_details}</p>
                </div>
                <div className="mt-4">
                  <div className="flex items-center mb-2">
                    <span className="text-yellow-500 text-xl">⭐</span>
                    <span className="text-lg font-semibold text-gray-900 ml-2">
                      {server.rating}/5
                    </span>
                    <span className="text-gray-600 ml-2">
                      ({server.total_reviews} reviews)
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div className="mb-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Detailed Description</h3>
              <p className="text-gray-700 leading-relaxed">{server.detailed_description}</p>
            </div>

            <div className="flex space-x-4">
              <button
                onClick={() => handleAffiliateClick(server)}
                className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-md hover:bg-blue-700 transition-colors font-semibold text-lg"
              >
                Get Started Now
              </button>
              <button
                onClick={() => {
                  trackClick(server.id, 'official');
                  window.open(server.official_url, '_blank');
                }}
                className="flex-1 border border-gray-300 text-gray-700 py-3 px-6 rounded-md hover:bg-gray-50 transition-colors font-semibold text-lg"
              >
                Official Website
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

function App() {
  const path = window.location.pathname;
  const serverId = path.match(/\/server\/(.+)/)?.[1];

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/directory" element={<DirectoryPage />} />
          <Route path="/server/:id" element={<ServerDetailPage serverId={serverId} />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;