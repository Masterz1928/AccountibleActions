import { useState, useEffect } from "react";

function App() {
  const [task, setTask] = useState([]);
  const [InputText, setSetInputText] = useState(""); 
  const handleToggle = () => {
    fetch(`http://127.0.0.1:8000/tasks/${taskId}/toggle`, {method: 'PUT'})
    .then(response = response.json)
    .then(data => {
      fetch(`http://127.0.0.1:8000/tasks/`)
        .then(response = response.json)
        .then(newData => setTask(newData.task));

    })
    .catch(error => console.error("Error Toggling: ", error))
  }
  
  // NEW 1: The Loading Memory
  const [isLoading, setIsLoading] = useState(false); 

  const handleDecompose = () => {
    // NEW 2: The Empty Input Shield
    if (InputText.trim() === "") {
        alert("Please type a task first!");
        return; // Stops the function immediately
    }

    // Turn the loading state ON
    setIsLoading(true); 
    console.log("Sending to AI:", InputText);

    fetch(`http://127.0.0.1:8000/decompose/?vague_task=${InputText}`, { 
        method: 'POST' 
    })
    .then(response => response.json())
    .then(data => {
        fetch('http://127.0.0.1:8000/tasks/')
          .then(response => response.json())
          .then(newData => {
              setTask(newData.task);
              setSetInputText(""); 
              
              // Turn the loading state OFF when finished!
              setIsLoading(false); 
          });
    })
    .catch(error => {
        console.error("Error talking to AI: ", error);
        setIsLoading(false); // Make sure it turns off even if there is an error!
    });
  };

  useEffect(() => {
    fetch('http://127.0.0.1:8000/tasks/')
      .then(response => response.json())
      .then(data => setTask(data.task))
      .catch(error => console.error(error));
  }, []); 

  return (
    <div style={{ padding: "20px" }}>
      <h1>AI Proactive To-Do List</h1>
      
      <div style={{ marginBottom: "30px", padding: "15px", backgroundColor: "#4f24e8", borderRadius: "8px" }}>
        <h3>Add a Task</h3>
        <input
          type="text"
          placeholder="e.g., Plan a Trip"
          value={InputText}
          onChange={(e) => setSetInputText(e.target.value)}
          style={{ padding: "10px", width: "60%", marginRight: "10px", borderRadius: "5px", border: "1px solid #ccc" }}
          // Disable the input box while loading!
          disabled={isLoading} 
        />
        
        {/* NEW 3: The Dynamic Button */}
        <button
          onClick={handleDecompose}
          disabled={isLoading} // Physically locks the button!
          style={{ 
            padding: "10px", 
            width: "30%", 
            borderRadius: "5px", 
            backgroundColor: isLoading ? "#cccccc" : "#007BFF", // Turns gray while loading
            color: "white", 
            border: "none", 
            cursor: isLoading ? "not-allowed" : "pointer" 
          }}
        >
          {/* Change the text based on the memory! */}
          {isLoading ? "✨ AI is thinking..." : "Simplify with AI ✨"}
        </button>
      </div>

    {task.map((singleTask) => (
            <div 
              key={singleTask.id} 
              style={{ 
                border: '1px solid black', 
                margin: '10px', 
                padding: '10px',
                // Turn the background green if it's done!
                backgroundColor: singleTask.completed ? "#d4edda" : "white", 
                // Cross out the text if it's done!
                textDecoration: singleTask.completed ? "line-through" : "none" 
              }}
            >
              {/* THE NEW CHECKBOX */}
              <label style={{ cursor: "pointer", display: "flex", alignItems: "center", gap: "10px" }}>
                <input 
                  type="checkbox" 
                  checked={singleTask.completed} 
                  onChange={() => handleToggle(singleTask.id)} 
                  style={{ transform: "scale(1.5)" }} // Make it a bit bigger
                />
                <h3 style={{ margin: 0 }}>{singleTask.title}</h3>
              </label>

              <p>{singleTask.description}</p>
              {singleTask.est_time && <p>⏱️ Est. Time: {singleTask.est_time} mins</p>}
            </div>
          ))}
    </div>
  );
}

export default App;