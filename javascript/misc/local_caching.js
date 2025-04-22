// CHAT-GPT VERSION
// Function to fetch and cache data from API
async function fetchData(url) {
    const cachedData = localStorage.getItem(url); // Check if data exists in cache
    if (cachedData) {
        const parsedData = JSON.parse(cachedData);
        
        // Check if cached data is still valid (e.g., check timestamp or TTL)
        if (Date.now() < parsedData.expiry) {
            console.log("Using cached data");
            return parsedData.value; // Return cached data if valid
        } else {
            localStorage.removeItem(url); // Expired data, remove it
        }
    }

    try {
        // If no valid cached data, fetch from API
        const response = await fetch(url);
        const data = await response.json();

        // Store the data with an expiry time (e.g., 1 hour)
        const cacheItem = {
            value: data,
            expiry: Date.now() + 60 * 60 * 1000, // 1 hour TTL
        };
        localStorage.setItem(url, JSON.stringify(cacheItem)); // Save to localStorage
        return data;
    } catch (error) {
        console.error("Error fetching data:", error);
        throw error; // Re-throw the error for handling downstream if needed
    }
}

// Example usage
(async () => {
    try {
        const data = await fetchData('https://api.example.com/data');
        console.log("API Data:", data);
    } catch (error) {
        console.error("Error:", error);
    }
})();

//////////////////////////////////////////////////////////////////////////////////////////


// GOOGLE GEMINI VERSION
// Function to fetch and cache data from API
async function fetchDataAndCache(apiUrl, cacheKey) {
    try {
      // Check if data exists in localStorage
      const cachedDataString = localStorage.getItem(cacheKey);
  
      if (cachedDataString) {
        const cachedData = JSON.parse(cachedDataString);
  
        // Optional: Check for data freshness (e.g., within the last hour)
        const timestamp = localStorage.getItem(`${cacheKey}_timestamp`);
        const now = Date.now();
        const cacheDuration = 60 * 60 * 1000; // 1 hour in milliseconds
  
        if (timestamp && (now - parseInt(timestamp, 10)) < cacheDuration) {
          console.log(`Using cached data for ${apiUrl}`);
          return cachedData;
        } else {
          console.log(`Cached data for ${apiUrl} is stale, fetching again.`);
          // Remove stale data from localStorage (optional)
          localStorage.removeItem(cacheKey);
          localStorage.removeItem(`${cacheKey}_timestamp`);
        }
      }
  
      // Data not in cache or stale, fetch from the API
      console.log(`Workspaceing data from ${apiUrl}`);
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
  
      // Store the fetched data in localStorage
      localStorage.setItem(cacheKey, JSON.stringify(data));
      localStorage.setItem(`${cacheKey}_timestamp`, Date.now());
  
      return data;
    } catch (error) {
      console.error(`Error fetching or caching data for ${apiUrl}:`, error);
      // You might want to return a default value or handle the error differently
      return null;
    }
  }
  
  // Example usage
  
  async function loadUserInfo() {
    const userInfo = await fetchDataAndCache('/api/user-info', 'userInfo');
    if (userInfo) {
      // Update your website elements with the user info
      document.getElementById('username').textContent = userInfo.name;
      document.getElementById('user-email').textContent = userInfo.email;
    }
  }
  
  // Call this function when your page loads
  loadUserInfo();