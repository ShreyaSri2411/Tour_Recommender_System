import streamlit as st
import requests
import streamlit.components.v1 as components


FASTAPI_URL = "http://localhost:8010/user_guide"
# FASTAPI_URL = "http://172.18.4.44:8010/user_guide"

def main():
    st.title("User Guide Recommender")

    area_type = st.selectbox("Select Area Type", ["Beach", "Adventure", "Religious", "Historical"]) 
    budget = st.number_input("Enter Budget", min_value=0.0, format="%.2f")
    description = st.text_area("Enter Description")

    if st.button("Get Recommendations"):
        payload = {
            "area_type": area_type,
            "budget": budget,
            "description": description
        }
        
        response = requests.post(FASTAPI_URL, json=payload)
        
        if response.status_code == 200:
            recommendations = response.json()
            
            st.subheader("Recommendations")
            for rec in recommendations:
                st.write(f"**Place:** {rec['places']}")
                st.write(f"**State:** {rec['state']}")
                st.write(f"**Type:** {rec['type']}")
                st.write(f"**Rating:** {rec['rating']}")
                st.write(f"**Description:** {rec['description']}")
                st.write(f"**Best Time to Visit:** {rec['best_time_to_visit']}")
                st.write(f"**Average Accommodation Cost (Rs/day):** {rec['avg_accommodation_cost/day(Rs)']}")
                st.write("---")
        else:
            st.error("Failed to fetch recommendations")

     # Tableau Dashboard Embed Code
    tableau_embed_code = """
    <div class='tableauPlaceholder' id='viz1723177845931' style='position: relative'>
        <noscript>
            <a href='#'>
                <img alt=' ' src='https://public.tableau.com/static/images/To/Tour_Recommender_System/Dashboard1/1_rss.png' style='border: none' />
            </a>
        </noscript>
        <object class='tableauViz' style='display:none;'>
            <param name='host_url' value='https://public.tableau.com/' />
            <param name='embed_code_version' value='3' />
            <param name='site_root' value='' />
            <param name='name' value='Tour_Recommender_System/Dashboard1' />
            <param name='tabs' value='yes' />
            <param name='toolbar' value='yes' />
            <param name='static_image' value='https://public.tableau.com/static/images/To/Tour_Recommender_System/Dashboard1/1.png' />
            <param name='animate_transition' value='yes' />
            <param name='display_static_image' value='yes' />
            <param name='display_spinner' value='yes' />
            <param name='display_overlay' value='yes' />
            <param name='display_count' value='yes' />
            <param name='language' value='en-US' />
        </object>
    </div>
    <script type='text/javascript'>
        var divElement = document.getElementById('viz1723177845931');
        var vizElement = divElement.getElementsByTagName('object')[0];
        if ( divElement.offsetWidth > 800 ) {
            vizElement.style.width='100%';
            vizElement.style.height=(divElement.offsetWidth*0.75)+'px';
        } else if ( divElement.offsetWidth > 500 ) {
            vizElement.style.width='100%';
            vizElement.style.height=(divElement.offsetWidth*0.75)+'px';
        } else {
            vizElement.style.width='100%';
            vizElement.style.minHeight='750px';
            vizElement.style.maxHeight=(divElement.offsetWidth*1.77)+'px';
        }
        var scriptElement = document.createElement('script');
        scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
        vizElement.parentNode.insertBefore(scriptElement, vizElement);
    </script>
    """

    # Embed Tableau dashboard in Streamlit
    components.html(tableau_embed_code, height=800)

          



if __name__ == "__main__":
    main()
