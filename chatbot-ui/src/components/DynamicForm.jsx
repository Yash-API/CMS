import { useState } from "react";

export default function DynamicForm({ fields, onSubmit, title }) {
  const [formData, setFormData] = useState({});

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="form-container">
      <h2 className="form-title">{title}</h2>
      <form onSubmit={handleSubmit} className="form-grid">
        {fields.map((field) => (
          <div key={field.name} className="form-field">
            <label>{field.label}</label>
            <input
              type={field.type}
              name={field.name}
              required={field.required}
              onChange={handleChange}
              className="form-input"
            />
          </div>
        ))}
        <button type="submit" className="form-submit-button">Submit</button>
      </form>
    </div>
  );
}
