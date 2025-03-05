async function fetchCurrentUser() {
  try {
    const response = await fetch("/get_current_user_info"); // Call Flask endpoint
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    const userData = await response.json();
    console.log("Current User:", userData); // Log or use user data
    return userData;
  } catch (error) {
    console.error("Failed to fetch user:", error);
  }
}

export { fetchCurrentUser };
