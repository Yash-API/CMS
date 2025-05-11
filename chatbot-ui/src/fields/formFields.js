export const employeeFields = [
    { name: "name", label: "Name", type: "text", required: true },
    { name: "role", label: "Role", type: "text", required: true },
    { name: "salary", label: "Salary", type: "number", required: true },
    { name: "joining_date", label: "Joining Date", type: "date", required: true },
    { name: "dob", label: "Date of Birth", type: "date", required: false },
  ];
  
  export const clientFields = [
    { name: "name", label: "Client Name", type: "text", required: true },
    { name: "budget", label: "Budget", type: "number", required: true },
    { name: "project_description", label: "Project Description", type: "text", required: true },
    { name: "project_start_date", label: "Project Start Date", type: "date", required: true },
    { name: "project_end_date", label: "Project End Date", type: "date", required: false },
  ];
  