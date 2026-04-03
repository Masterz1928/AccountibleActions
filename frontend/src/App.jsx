import { useState, useEffect } from "react";

function App() {
  console.log("TRIPWIRE 1: React is rendering the page!");

  const [task, setTask] = useState([]);

  useEffect(() => {
    console.log("TRIPWIRE 2: useEffect triggered, trying to fetch...");
    
    fetch('http://127.0.0.1:8000/tasks/')
      .then(response => {
        console.log("TRIPWIRE 3: Server responded! Unpacking JSON...");
        return response.json(); // CRITICAL: Must have the () here
      })
      .then(data => {
        console.log("TRIPWIRE 4: SUCCESS! Here is the data:", data);
        setTask(data.task);
      })
      .catch(error => console.error("TRIPWIRE 5: ERROR CAUGHT: ", error));
  }, []); 

  return (
    <div style={{ padding: "20px" }}>
      <h1>🧠 AI Proactive To-Do List</h1>
      <p>If you see this, React is displaying HTML.</p>
      {task.map((singleTask) => (
        <div key={singleTask.id} style={{ border: '1px solid black', margin: '10px', padding: '10px' }}>
          <h3>{singleTask.title}</h3>
          <p>{singleTask.description}</p>
        </div>
      ))}
    </div>

  );
}


export default App;