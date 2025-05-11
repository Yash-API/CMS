import DynamicForm from "./components/DynamicForm";
import { employeeFields, clientFields } from "./fields/formFields";
import axios from "axios";
import { useParams } from "react-router-dom";

const API_URL = import.meta.env.VITE_API_URL;

export default function AddUser() {
  const { type } = useParams(); // expect either "employee" or "client"
  const fields = type === "employee" ? employeeFields : clientFields;

  const handleSubmit = async (data) => {
    try {
      await axios.post(`${API_URL}/api/${type}s`, data);
      alert(`${type} added successfully`);
    } catch (err) {
      console.error(err);
      alert("Failed to add " + type);
    }
  };

  return (
    <DynamicForm
      fields={fields}
      onSubmit={handleSubmit}
      title={`Add New ${type.charAt(0).toUpperCase() + type.slice(1)}`}
    />
  );
}
