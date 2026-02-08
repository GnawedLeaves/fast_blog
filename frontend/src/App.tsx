import axios from "axios";
import dayjs from "dayjs";
import { useEffect, useState } from "react";
import "./App.css";
import type { Post } from "./types";

function App() {
  const [posts, setPosts] = useState<Post[]>([]);

  const BASE_URL = "http://127.0.0.1:8000";
  const handleGetPosts = () => {
    axios
      .get(BASE_URL + "/api/allPosts")
      .then((response) => {
        setPosts(response.data);
      })
      .catch((error) => {
        console.error("There was an error fetching the posts uh oh", error);
      });
  };

  useEffect(() => {
    handleGetPosts();
  }, []);

  return (
    <div>
      <div className="w-100">
        <h1 className="mb-8">Super Blog</h1>
        <div className="flex-center flex-col gap-8">
          {posts.map((post) => {
            return (
              <div className="flex-center flex-col border border-amber-50 rounded-xl p-4 w-100">
                <div className="text-3xl">{post.title}</div>
                <div className="flex justify-between items-center w-full ">
                  <div className="flex items-center gap-2">
                    <img
                      src={post.author.image_path}
                      className="border-2 border-amber-600 w-9 h-9 rounded-full object-cover"
                    />
                    <div className="flex flex-col text-left">
                      <div className="text-sm ">{post.author.username}</div>
                      <div className="text-sm text-zinc-400">
                        {post.author.email}
                      </div>
                    </div>
                  </div>
                  <div className="text-zinc-500 text-xs self-end">
                    {dayjs(post.date_posted).format("DD MMM YYYY HH:mm")}
                  </div>
                </div>

                <div className="mt-6  w-full text-left">{post.content}</div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default App;
