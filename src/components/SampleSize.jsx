import React from 'react'
import ClipLoader from "react-spinners/ClipLoader";
import { Checkbox } from '@mui/material'
import { useState } from 'react'
import "./samplesize.css"
import { Table, TableHead, TableBody, TableRow, TableCell } from '@mui/material';
const SampleSizeUpdated = () => {
    const [type,setType] = useState("select")
    const [sKnown,setSKnown] = useState(false)
    const [standard_deviation,set_standard_deviation]=useState(null)
    const [conf,set_conf]=useState(false)
    const [population_size,set_population_size] = useState(null)
    const [error,setError]=useState(0)
    const [confidence_level,set_confidence_level]=useState(0.90)
    const [toggle,setToggle] = useState(false)
    const [buttonClicked,setButtonClicked] = useState(false)
    const [data,setData] = useState({});    
    const[PopInfoClicked,setPopInfoClicked]=useState(false)
    const[errorInfoClicked,setErrorInfoClicked]=useState(false)
    const[deviationInfoClicked,setDeviationInfoClicked]=useState(false)
    const [confidenceInfoClicked,setConfidenceInfoClicked]=useState(false)
    const handleSubmit =async () => 
{
 
setButtonClicked(true)

var data;
if(conf){
 data =
    {
    population_size,
    error,
    standard_deviation,
    confidence_level 
    }
  }
  else if(!conf)
  {
    data =
    {
    population_size,
    error,
    standard_deviation,
    }
  }
console.log(data)
 fetch("https://100102.pythonanywhere.com/sample-size/", {
//  fetch("http://127.0.0.1:8000/sample-size/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(data),
})

  .then((response) => response.json())
  .then((data) => {
    if(data.error)
    {
      console.log('Error data, ', data.error)
      alert("Check your inputs!")
      setButtonClicked(false)
    }
    else
    {

      setData(data)
      setToggle(true)
      setButtonClicked(false)
    }
    //   console.log(data);
    
  })
  .catch((error) => {
    // Handle any errors that occurred during the request
  });
 
    // }

}

  return (
    <div>
        <div className='mobile'>
         <h1 >Sample Size</h1>
         <p>Type:</p>
    <select className="form-control form-control-lg" onChange={e=>setType(e.target.value)}>
        <option value="select">--select--</option>
        <option value="finite">Finite Population</option>
        <option value="infinite">Infinite Population</option>
    </select>
        <div style={{display:"flex",padding:"1em",justifyContent:"space-between",gap:"5em"}}>
            <div style={{width:"50%",display:"grid",gap:"1em"}}>
                { type !== "select" &&
                <>
                {type === "finite" &&
                <>
                    <label className="form-label">Population Size:<button className='infoButton' onClick={e=>setPopInfoClicked(!PopInfoClicked)}>?</button> {PopInfoClicked && <span className='info'>(The total number of individuals or elements in the entire population being studied. It is the entire group from which a  sample is drawn.)</span>}</label>
      <input  class="form-control" placeholder='Enter N'  onChange={e=>set_population_size(e.target.value)} type='number' />
      </> }
        <div style={{display:"flex"}}> 
         <label>Standard Deviation: <button className='infoButton' onClick={e=>setDeviationInfoClicked(!deviationInfoClicked)}>?</button>{deviationInfoClicked && <span className='info'>(A measure of how much the values in a dataset differ from the mean. It indicates the spread or dispersion of the data points.)</span>}</label>
        <Checkbox  style={{marginTop:"-9px"}} onChange={e=>setSKnown(!sKnown)}/>
        </div>
            {
                sKnown &&
                <input class="form-control" placeholder='Enter Standard Deviation' onChange={e=>set_standard_deviation(e.target.value)} type='number'/>}
      <label className="form-label">Error:<button className='infoButton' onClick={e=>setErrorInfoClicked(!errorInfoClicked)}>?</button> {errorInfoClicked && <span className='info'>(Imagine you're conducting a survey, and you want to know what percentage of people in your town like ice cream. You survey 500 people and find that 60% of them like ice cream.

However, you know that not everyone in your town was surveyed. So, there's a chance that if you surveyed everyone, the percentage might be slightly different.

The margin of error is like a safety net around your survey result. It tells you how much your result might vary if you surveyed everyone. If your margin of error is ±5%, it means that the true percentage of people who like ice cream could be as low as 55% or as high as 65%, with 95% confidence.

In simple terms, a confidence interval gives you a range of values where you think the true answer lies, and the margin of error tells you how much that range might wiggle if you talked to more people or collected more data. It's a way of being honest about the uncertainty in your estimates.)</span>}</label>
       <input type='number' className="form-control form-control-lg" placeholder='Error'  style={{width:"200px"}} onChange={e=>setError(e.target.value)}/>
         <div style={{display:"flex"}}> 
         <label>Confidence Level:<button className='infoButton' onClick={e=>setConfidenceInfoClicked(!confidenceInfoClicked)}>?</button>{confidenceInfoClicked && <span className='info'>(Imagine you're trying to estimate something, like the average height of all students in your school. You can't measure every single student's height; that would take too much time and effort. So, you decide to measure the heights of a sample, say 100 students.

Now, here's where the confidence interval comes in. Instead of giving a single number as your estimate (e.g., the average height is 160 cm), you give a range of values (e.g., 155 cm to 165 cm) along with a level of confidence (e.g., 95%).

What this means is that you're saying, "I'm 95% confident that the real average height of all students falls between 155 cm and 165 cm based on my sample." In other words, you acknowledge that your estimate might not be perfect, but you're pretty sure it's in that range.)</span>}</label>
        <Checkbox  style={{marginTop:"-9px"}} onChange={e=>set_conf(!conf)}/>
        </div>
       {
        conf && <>
        <label className="form-label">Confidence Level:</label>
       <select className="form-control form-control-lg" onChange={(e)=>set_confidence_level(e.target.value)}>
        <option disabled>--select--</option>
        <option>0.90</option>
        <option>0.95</option>
        <option>0.99</option>
        </select>
        </>
        }
        <button onClick={handleSubmit} className="btn btn-primary" disabled={buttonClicked} >Submit</button>
  </>
  }     
       </div>
            <div style={{width:"50%"}}>
                {toggle  && 
 
<>
                    <h2 style={{marginTop:"2em",display:"grid",justifyContent:"center"}}>Response</h2>
  <Table className="styled-table">
          <TableHead>
            <TableRow >
              <TableCell style={{fontWeight:"bolder"}}>Sample Size</TableCell>
              <TableCell style={{fontWeight:"bolder"}}>Process Time</TableCell>
              <TableCell style={{fontWeight:"bolder"}}>Method Used</TableCell>
              {/* Add more TableCell elements for additional columns */}
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell>{data.sample_size}</TableCell>
              <TableCell>{data.process_time}</TableCell>
              <TableCell>{data.method_used}</TableCell>
              {/* Add more TableCell elements for additional columns */}
            </TableRow>
          </TableBody>
          </Table>
</>
}
            </div>
        </div>
        {!toggle && buttonClicked &&
 
     <div style={{marginLeft:"30%",justifyContent:"center"}}> 
      <ClipLoader
        color="green"
        loading={true}
        size={50}
        aria-label="Loading Spinner"
        data-testid="loader"
      />
      </div>
 
 }
 {toggle &&
    <>
        <button onClick={e=>window.location.reload("/")} className="btn btn-primary"  >Try Again</button>
    </>
    }
        </div>
      
    </div>
  )
}

export default SampleSizeUpdated
