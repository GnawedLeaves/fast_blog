import {
  Button,
  Card,
  Divider,
  Flex,
  Form,
  Input,
  message,
  Popconfirm,
  Select,
} from "antd";
import dayjs from "dayjs";
import { useEffect, useState } from "react";
import "./App.css";
import PostController from "./service/PostController";
import UserController from "./service/UserController";
import type { Post, User } from "./types";

function App() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [showCreateCard, setShowCreateCard] = useState<boolean>(false);
  const [editingPost, setEditingPost] = useState<Post | null>(null);

  const { getAllPosts, createPost, updatePost, deletePost } = PostController();
  const { getAllUsers } = UserController();
  const [form] = Form.useForm();

  const loadData = async () => {
    const [fetchedPosts, fetchedUsers] = await Promise.all([
      getAllPosts(),
      getAllUsers(),
    ]);
    setPosts(fetchedPosts);
    setUsers(fetchedUsers);
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleFinish = async (values: any) => {
    if (editingPost) {
      const success = await updatePost(editingPost.id, values);
      if (success) {
        message.success("Post updated!");
        setEditingPost(null);
      }
    } else {
      const success = await createPost(values);
      if (success) {
        message.success("Post created!");
      }
    }
    form.resetFields();
    setShowCreateCard(false);
    loadData();
  };

  const handleDelete = async (id: number) => {
    const success = await deletePost(id);
    if (success) {
      message.success("Post deleted");
      loadData();
    }
  };

  const startEdit = (post: Post) => {
    setEditingPost(post);
    setShowCreateCard(true);
    form.setFieldsValue({
      title: post.title,
      content: post.content,
      user_id: post.author.id,
    });
  };

  return (
    <div className="w-100 p-4">
      <div className="flex justify-between items-center mb-8">
        <h1>Super Blog</h1>
        <Button
          type="primary"
          onClick={() => {
            setEditingPost(null);
            form.resetFields();
            setShowCreateCard(true);
          }}
        >
          Add Post
        </Button>
      </div>

      {showCreateCard && (
        <Card title={editingPost ? "Edit Post" : "New Post"} className="mb-8">
          <Form form={form} layout="vertical" onFinish={handleFinish}>
            <Form.Item
              name="user_id"
              label="Author"
              rules={[{ required: true, message: "Author is required" }]}
            >
              <Select
                disabled={!!editingPost}
                options={users.map((u) => ({ label: u.username, value: u.id }))}
                placeholder="Select an author"
              />
            </Form.Item>
            <Form.Item
              name="title"
              label="Title"
              rules={[
                { required: true, message: "Title is required" },
                {
                  max: 15,
                  message: "Title cannot be longer than 15 characters",
                },
              ]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              name="content"
              label="Content"
              rules={[{ required: true, message: "Content is required" }]}
            >
              <Input.TextArea rows={4} />
            </Form.Item>
            <Flex gap="middle">
              <Button onClick={() => setShowCreateCard(false)} block>
                Cancel
              </Button>
              <Button type="primary" htmlType="submit" block>
                {editingPost ? "Update" : "Publish"}
              </Button>
            </Flex>
          </Form>
        </Card>
      )}

      <div className="flex flex-col gap-6">
        {posts.map((post) => (
          <div
            key={post.id}
            className="border border-amber-50 rounded-xl p-6 w-100 bg-zinc-900"
          >
            <div className="flex justify-between items-start">
              <div className="text-3xl font-bold mb-4">{post.title}</div>
              <Flex gap="small">
                <Button size="small" onClick={() => startEdit(post)}>
                  Edit
                </Button>
                <Popconfirm
                  title="Delete post?"
                  onConfirm={() => handleDelete(post.id)}
                >
                  <Button size="small" danger>
                    Delete
                  </Button>
                </Popconfirm>
              </Flex>
            </div>

            <div className="flex justify-between items-center w-full">
              <Flex align="center" gap="small">
                <img
                  src={post.author.image_path}
                  className="border-2 border-amber-600 w-10 h-10 rounded-full object-cover"
                />
                <div className="text-left">
                  <div className="text-sm font-semibold">
                    {post.author.username}
                  </div>
                  <div className="text-xs text-zinc-400">
                    {post.author.email}
                  </div>
                </div>
              </Flex>
              <div className="text-zinc-500 text-xs">
                {dayjs(post.date_posted).format("DD MMM YYYY HH:mm")}
              </div>
            </div>
            <Divider className="my-4" />
            <div className="text-left text-zinc-200 leading-relaxed">
              {post.content}
            </div>
          </div>
        ))}
        {posts.length === 0 && "No posts yet :("}
      </div>
    </div>
  );
}

export default App;
