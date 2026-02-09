import axios from "axios";
import type { Post, User } from "../types";

const PostController = () => {
  const BASE_URL = "http://127.0.0.1:8000";

  const getAllPosts = async (): Promise<Post[]> => {
    try {
      const response = await axios.get(`${BASE_URL}/api/allPosts`);
      return response.data;
    } catch (e) {
      console.error("there was an error fetching the posts uh oh", e);
      return [];
    }
  };

  const getAllUsers = async (): Promise<User[]> => {
    try {
      const response = await axios.get(`${BASE_URL}/api/allUsers`);
      return response.data;
    } catch (e) {
      console.error("error fetching users", e);
      return [];
    }
  };

  return { getAllPosts, getAllUsers };
};
export default PostController;
