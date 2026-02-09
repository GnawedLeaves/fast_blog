import axios from "axios";
import type { User } from "../types";
const BASE_URL = "http://127.0.0.1:8000";

const UserController = () => {
  const getAllUsers = async (): Promise<User[]> => {
    try {
      const response = await axios.get(`${BASE_URL}/api/allUsers`);
      return response.data;
    } catch (e) {
      console.error("Error fetching users:", e);
      return [];
    }
  };

  const getUserById = async (userId: number): Promise<User | null> => {
    try {
      const response = await axios.get(`${BASE_URL}/api/users/${userId}`);
      return response.data;
    } catch (e) {
      console.error("Error fetching user:", e);
      return null;
    }
  };

  const createUser = async (userData: {
    username: string;
    email: string;
  }): Promise<User | null> => {
    try {
      const response = await axios.post(`${BASE_URL}/api/users`, userData);
      return response.data;
    } catch (e) {
      console.error("Error creating user:", e);
      return null;
    }
  };

  return {
    getAllUsers,
    getUserById,
    createUser,
  };
};

export default UserController;
