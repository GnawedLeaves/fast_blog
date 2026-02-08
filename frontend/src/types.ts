export interface User {
  username: string;
  email: string;
  id: number;
  image_file: string;
  image_path: string;
}

export interface Post {
  title: string;
  content: string;
  id: number;
  user_id: number;
  date_posted: string;
  author: User;
}
