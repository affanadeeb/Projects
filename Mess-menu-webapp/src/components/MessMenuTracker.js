import React, { useState, useEffect } from 'react';
import { read } from 'xlsx';
import { MealCard } from './MealCard';
import { parseExcelData } from '../utils/parseExcelData';
import { FaGithub } from 'react-icons/fa';
import { motion } from 'framer-motion';

const getDayOfWeek = () => {
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  return days[new Date().getDay()];
};

const MessMenuTracker = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [selectedDay, setSelectedDay] = useState(getDayOfWeek());
  const [selectedMess, setSelectedMess] = useState('');
  const [messMenus, setMessMenus] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMenuData = async () => {
      try {
        const messFiles = ['yuktahaar', 'kadamba', 'north', 'south'];
        const menus = {};

        for (const mess of messFiles) {
          try {
            const response = await fetch(`/data/${mess}.xlsx`);
            if (!response.ok) {
              throw new Error(`HTTP error ${response.status}`);
            }
            const arrayBuffer = await response.arrayBuffer();
            const workbook = read(arrayBuffer);
            const worksheet = workbook.Sheets[workbook.SheetNames[0]];
            menus[mess] = parseExcelData(worksheet);
          } catch (messError) {
            console.error(`Error loading ${mess} menu:`, messError);
            menus[mess] = {
              breakfast: { [selectedDay.toLowerCase()]: ['Menu not available'] },
              lunch: { [selectedDay.toLowerCase()]: ['Menu not available'] },
              snacks: { [selectedDay.toLowerCase()]: ['Menu not available'] },
              dinner: { [selectedDay.toLowerCase()]: ['Menu not available'] }
            };
          }
        }

        setMessMenus(menus);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching menu data:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchMenuData();

    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 60000);

    return () => clearInterval(timer);
  }, []);

  const getCurrentMenuItems = (menu) => {
    const dayKey = selectedDay.toLowerCase();
    return {
      breakfast: menu.breakfast[dayKey] || ['Menu not available'],
      lunch: menu.lunch[dayKey] || ['Menu not available'],
      snacks: menu.snacks[dayKey] || ['Menu not available'],
      dinner: menu.dinner[dayKey] || ['Menu not available']
    };
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600">
        <div className="bg-white p-8 rounded-lg shadow-xl">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500 mx-auto"></div>
          <p className="text-xl mt-4 text-gray-700">Loading menu data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-red-500 to-pink-600">
        <div className="bg-white p-8 rounded-lg shadow-xl">
          <p className="text-xl text-red-500">Error: {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-8 relative">
      <div className="container mx-auto px-4 pb-16"> {/* Added padding bottom for footer */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">IIIT-H Mess Menu</h1>
          <p className="text-lg text-gray-600">
            {currentTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </p>
        </div>

        <div className="flex flex-col sm:flex-row justify-center gap-4 mb-8">
          <select
            value={selectedDay}
            onChange={(e) => setSelectedDay(e.target.value)}
            className="px-4 py-2 rounded-lg border-2 border-purple-200 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 outline-none transition-all"
          >
            {['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'].map(day => (
              <option key={day} value={day}>{day}</option>
            ))}
          </select>

          <select
            value={selectedMess}
            onChange={(e) => setSelectedMess(e.target.value)}
            className="px-4 py-2 rounded-lg border-2 border-purple-200 focus:border-purple-400 focus:ring-2 focus:ring-purple-200 outline-none transition-all"
          >
            <option value="">Select Mess</option>
            <option value="yuktahaar">Yuktahaar</option>
            <option value="kadamba">Kadamba</option>
            <option value="north">North</option>
            <option value="south">South</option>
          </select>
        </div>

        {selectedMess && messMenus[selectedMess] && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {Object.entries(getCurrentMenuItems(messMenus[selectedMess])).map(([meal, items]) => (
              <MealCard
                key={`${selectedMess}-${meal}`}
                messName={meal.charAt(0).toUpperCase() + meal.slice(1)}
                menuItems={items}
                currentMeal={meal.toUpperCase()}
              />
            ))}
          </div>
        )}

        {/* Footer with GitHub Link */}
        <footer className="fixed bottom-0 left-0 right-0 bg-white bg-opacity-90 shadow-lg py-4">
          <div className="container mx-auto px-4">
            <div className="flex flex-col sm:flex-row justify-center items-center gap-4 text-center">
              <div className="flex items-center gap-2">
                <FaGithub className="w-5 h-5 text-gray-700" />
                <a
                  href="https://github.com/affanadeeb/dining-iiit" // Replace with your GitHub repository URL
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 font-medium transition-colors"
                >
                  View Source Code
                </a>
              </div>
              <span className="hidden sm:inline text-gray-400">|</span>
              <p className="text-gray-600">
                Made with ❤️ for IIIT-H Students
              </p>
              <span className="hidden sm:inline text-gray-400">|</span>
              <p className="text-gray-500 text-sm">
                Want to update the menu? Fork the repository and submit a PR!
              </p>
              <span className="hidden sm:inline text-gray-400">|</span>
              <p className="text-gray-500 text-xs">
                by Affan Shaik ✌️
              </p>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default MessMenuTracker;
