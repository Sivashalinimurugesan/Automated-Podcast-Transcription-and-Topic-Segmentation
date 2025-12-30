import "./Home.css";
//import Nav from "../components/Nav";
import UploadCard from "../components/UploadCard";
import Features from "../components/Features";
import HowItWorks from "../components/HowItWorks";
export default function Home(){
    return(
        <div>
            
            <h1 className="heading">
  Transform Podcasts into <br />
  <span className="gradient-text">Searchable Knowledge</span>
</h1>
            <p>Automatically transcribe podcast audio and segment into distinct topical sections.</p>
            <p>Navigate efficienty by browsing topics and key discussion point without listening to the entire episode</p>

<UploadCard />
<Features/>
<HowItWorks/>
        </div>
    );
}