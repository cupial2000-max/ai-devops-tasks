/**
 * Pobiera dane użytkownika z API i zwraca wybrane pola.
 * Przy statusie innym niż 2xx albo przy błędzie sieci wypisuje komunikat i zwraca null.
 *
 * @param {number|string} userId - Identyfikator użytkownika w ścieżce /users/{userId}.
 * @returns {Promise<{name: string, email: string, lastLogin: Date}|null>} Imię, e-mail i data ostatniego logowania albo null, gdy żądanie się nie powiedzie.
 */
function fetchUserData(userId) {
  return fetch(`https://api.example.com/users/${userId}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      return {
        name: data.name,
        email: data.email,
        lastLogin: new Date(data.lastLoginTimestamp)
      };
    })
    .catch(error => {
      console.error('Fetch error:', error);
      return null;
    });
}
