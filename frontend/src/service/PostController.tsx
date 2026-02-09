import axios from "axios";
import type { Post } from "../types";

const BASE_URL = "http://127.0.0.1:8000";

const PostController = () => {
  const getAllPosts = async (): Promise<Post[]> => {
    try {
      const response = await axios.get(`${BASE_URL}/api/allPosts`);
      return response.data;
    } catch (e) {
      console.error("Error fetching posts:", e);
      return [];
    }
  };

  const createPost = async (postData: {
    title: string;
    content: string;
    user_id: number;
  }): Promise<Post | null> => {
    try {
      const response = await axios.post(`${BASE_URL}/api/posts`, postData);
      return response.data;
    } catch (e) {
      console.error("Error creating post:", e);
      return null;
    }
  };

  const updatePost = async (
    postId: number,
    postData: Partial<Post>,
  ): Promise<Post | null> => {
    try {
      const response = await axios.patch(
        `${BASE_URL}/api/posts/${postId}`,
        postData,
      );
      return response.data;
    } catch (e) {
      console.error("Error updating post:", e);
      return null;
    }
  };

  const deletePost = async (postId: number): Promise<boolean> => {
    try {
      await axios.delete(`${BASE_URL}/api/posts/${postId}`);
      return true;
    } catch (e) {
      console.error("Error deleting post:", e);
      return false;
    }
  };

  return {
    getAllPosts,
    createPost,
    updatePost,
    deletePost,
  };
};

export default PostController;
