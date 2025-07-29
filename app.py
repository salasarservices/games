import streamlit as st
import time
import random

# Page configuration
st.set_page_config(
    page_title="Suraksha Shakti - Insurance Game",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Indian theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #FF9933, #FFFFFF, #138808);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: #000000;
    }
    
    .scenario-card {
        background: linear-gradient(135deg, #FFF8E1, #FFECB3);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #FF9800;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        color: #000000;
    }
    
    .choice-card {
        background: white;
        border: 2px solid #E0E0E0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
        color: #000000;
    }
    
    .choice-card:hover {
        border-color: #FF9800;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 152, 0, 0.2);
    }
    
    .stats-container {
        background: linear-gradient(135deg, #E8F5E8, #C8E6C9);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: #000000;
    }
    
    .result-good {
        background: linear-gradient(135deg, #E8F5E8, #C8E6C9);
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #000000;
    }
    
    .result-bad {
        background: linear-gradient(135deg, #FFEBEE, #FFCDD2);
        border: 2px solid #F44336;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #000000;
    }
    
    .final-grade {
        text-align: center;
        font-size: 4rem;
        font-weight: bold;
        margin: 2rem 0;
    }
    
    .hindi-text {
        font-family: 'Noto Sans Devanagari', sans-serif;
        font-size: 1.1rem;
        color: #333333;
        font-style: italic;
    }
    
    /* Fix button text color */
    .stButton > button {
        color: #000000 !important;
    }
    
    /* Ensure all text is black */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'money': 500000,  # 5 lakh rupees starting savings
        'coverage': 0,
        'current_scenario': 0,
        'insurance_types': [],
        'game_started': False,
        'choice_made': False,
        'event_shown': False
    }

# Game scenarios with Indian context
scenarios = [
    {
        'title': '🏠 अपना घर - Dream Home Purchase',
        'hindi_title': 'सपनों का घर खरीदना',
        'text': '''Congratulations! You've saved enough to buy your dream 2BHK flat in Delhi for ₹50 lakhs! 
        Your family is excited, but Mama ji warns: "Beta, Delhi mein anything can happen - floods, earthquakes, theft!"
        
        What home insurance will you choose to protect your family's biggest investment?''',
        'choices': [
            {
                'title': 'Basic Home Insurance (₹8,000/year)',
                'description': 'Covers fire, theft, and basic damages. Coverage: ₹30 lakhs',
                'hindi': 'बुनियादी गृह बीमा - आग, चोरी से सुरक्षा',
                'cost': 8000,
                'coverage': 3000000,
                'type': 'home_basic'
            },
            {
                'title': 'Comprehensive Home Insurance (₹15,000/year)',
                'description': 'Full replacement + natural disasters + contents. Coverage: ₹60 lakhs',
                'hindi': 'व्यापक गृह बीमा - पूर्ण सुरक्षा',
                'cost': 15000,
                'coverage': 6000000,
                'type': 'home_comprehensive'
            },
            {
                'title': 'No Insurance - "Bhagwan bharose"',
                'description': 'Save money now, pray nothing bad happens',
                'hindi': 'कोई बीमा नहीं - भगवान भरोसे',
                'cost': 0,
                'coverage': 0,
                'type': 'none'
            }
        ],
        'event': {
            'title': '🌊 Delhi Floods Strike!',
            'description': '''Heavy monsoon rains flood your building! Water damage ruins furniture, 
            electronics, and requires major repairs. Your neighbors are devastated.
            
            Total damage: ₹4 lakh''',
            'hindi': 'दिल्ली में बाढ़ - भारी नुकसान!',
            'damage': 400000
        }
    },
    {
        'title': '🏍️ नई बाइक - Two-Wheeler Dreams',
        'hindi_title': 'नई मोटरसाइकिल',
        'text': '''You've bought a shiny new Royal Enfield worth ₹2.5 lakhs! Perfect for those weekend rides to Gurgaon.
        
        But Papa reminds you: "Beta, Delhi traffic is crazy! And what about accidents?"
        
        Choose your two-wheeler insurance wisely:''',
        'choices': [
            {
                'title': 'Third-Party Only (₹2,000/year)',
                'description': 'Minimum legal requirement. Covers others, not your bike',
                'hindi': 'केवल तृतीय पक्ष बीमा - कानूनी न्यूनतम',
                'cost': 2000,
                'coverage': 0,
                'type': 'vehicle_third_party'
            },
            {
                'title': 'Comprehensive Insurance (₹8,000/year)',
                'description': 'Own damage + theft + third party. Coverage: ₹2.5 lakhs',
                'hindi': 'व्यापक वाहन बीमा - पूर्ण सुरक्षा',
                'cost': 8000,
                'coverage': 250000,
                'type': 'vehicle_comprehensive'
            },
            {
                'title': 'Premium with Zero Depreciation (₹12,000/year)',
                'description': 'Full coverage + no depreciation + roadside assistance',
                'hindi': 'प्रीमियम बीमा - शून्य मूल्यह्रास',
                'cost': 12000,
                'coverage': 300000,
                'type': 'vehicle_premium'
            }
        ],
        'event': {
            'title': '💥 Delhi Traffic Accident!',
            'description': '''While navigating through Connaught Place traffic, a car hits your bike!
            Your Royal Enfield needs major repairs and you're injured too.
            
            Bike repair cost: ₹1.2 lakhs
            Medical expenses: ₹50,000''',
            'hindi': 'दिल्ली ट्रैफिक में दुर्घटना!',
            'damage': 170000
        }
    },
    {
        'title': '👨‍👩‍👧‍👦 परिवार की जिम्मेदारी - Family Responsibilities',
        'hindi_title': 'परिवार की देखभाल',
        'text': '''You're now 30 and the primary earner. Wife, 2 kids, and aging parents depend on you.
        Your salary is ₹8 lakhs per year, but what if something happens to you?
        
        Bhabhi ji next door lost her husband suddenly - now she struggles financially.
        
        Think about your family's future:''',
        'choices': [
            {
                'title': 'Term Life Insurance (₹12,000/year)',
                'description': '20-year term, ₹1 crore coverage for family',
                'hindi': 'टर्म जीवन बीमा - परिवार के लिए',
                'cost': 12000,
                'coverage': 10000000,
                'type': 'life_term'
            },
            {
                'title': 'Endowment Policy (₹60,000/year)',
                'description': 'Insurance + investment, ₹25 lakhs coverage + returns',
                'hindi': 'एंडोमेंट पॉलिसी - बीमा और निवेश',
                'cost': 60000,
                'coverage': 2500000,
                'type': 'life_endowment'
            },
            {
                'title': 'Skip Life Insurance',
                'description': '"Main toh abhi young hun, kya zarurat hai"',
                'hindi': 'जीवन बीमा नहीं - अभी तो जवान हूं',
                'cost': 0,
                'coverage': 0,
                'type': 'none'
            }
        ],
        'event': {
            'title': '🏥 Serious Heart Attack!',
            'description': '''The stress of city life catches up! You suffer a major heart attack and need emergency surgery.
            
            Hospital bills: ₹8 lakhs
            Lost income during recovery: ₹3 lakhs
            Family expenses continue...''',
            'hindi': 'गंभीर दिल का दौरा!',
            'damage': 1100000
        }
    },
    {
        'title': '🏥 स्वास्थ्य चिंताएं - Health is Wealth',
        'hindi_title': 'स्वास्थ्य ही धन है',
        'text': '''Your company offers health insurance, but is it enough? Delhi's pollution, 
        stress, and lifestyle diseases are increasing. Private hospitals are expensive!
        
        Your colleague's father's cancer treatment cost ₹15 lakhs out of pocket.
        
        How will you protect your family's health?''',
        'choices': [
            {
                'title': 'Company Health Insurance (Free)',
                'description': '₹3 lakh coverage, limited hospitals, long waiting',
                'hindi': 'कंपनी स्वास्थ्य बीमा - मुफ्त लेकिन सीमित',
                'cost': 0,
                'coverage': 300000,
                'type': 'health_company'
            },
            {
                'title': 'Top-up Health Plan (₹15,000/year)',
                'description': '₹10 lakh additional coverage, cashless treatment',
                'hindi': 'टॉप-अप स्वास्थ्य योजना - अतिरिक्त कवरेज',
                'cost': 15000,
                'coverage': 1300000,
                'type': 'health_topup'
            },
            {
                'title': 'Premium Family Floater (₹45,000/year)',
                'description': '₹25 lakh family coverage, best hospitals, no waiting',
                'hindi': 'प्रीमियम पारिवारिक फ्लोटर - सर्वोत्तम',
                'cost': 45000,
                'coverage': 2500000,
                'type': 'health_premium'
            }
        ],
        'event': {
            'title': '🚑 Family Medical Emergency!',
            'description': '''Your mother needs emergency surgery for gallbladder stones, and your child breaks 
            his arm playing cricket. Both need immediate treatment at a private hospital.
            
            Mother's surgery: ₹4 lakhs
            Child's treatment: ₹1.5 lakhs
            Total medical emergency: ₹5.5 lakhs''',
            'hindi': 'पारिवारिक चिकित्सा आपातकाल!',
            'damage': 550000
        }
    }
]

def format_currency(amount):
    """Format currency in Indian format"""
    if amount >= 10000000:  # 1 crore
        return f"₹{amount/10000000:.1f} crore"
    elif amount >= 100000:  # 1 lakh
        return f"₹{amount/100000:.1f} lakh"
    else:
        return f"₹{amount:,}"

def reset_game():
    """Reset the game state"""
    st.session_state.game_state = {
        'money': 500000,
        'coverage': 0,
        'current_scenario': 0,
        'insurance_types': [],
        'game_started': False,
        'choice_made': False,
        'event_shown': False
    }

def make_choice(choice_index):
    """Process player's choice"""
    scenario = scenarios[st.session_state.game_state['current_scenario']]
    choice = scenario['choices'][choice_index]
    
    # Apply choice effects
    st.session_state.game_state['money'] -= choice['cost']
    st.session_state.game_state['coverage'] += choice['coverage']
    st.session_state.game_state['insurance_types'].append(choice['type'])
    st.session_state.game_state['choice_made'] = True
    st.session_state.selected_choice = choice

def show_event():
    """Show the random event and its consequences"""
    scenario = scenarios[st.session_state.game_state['current_scenario']]
    choice = st.session_state.selected_choice
    event = scenario['event']
    
    damage = event['damage']
    covered = min(damage, choice['coverage'])
    out_of_pocket = damage - covered
    
    st.session_state.game_state['money'] -= out_of_pocket
    st.session_state.game_state['event_shown'] = True
    
    return event, covered, out_of_pocket

def next_scenario():
    """Move to next scenario"""
    st.session_state.game_state['current_scenario'] += 1
    st.session_state.game_state['choice_made'] = False
    st.session_state.game_state['event_shown'] = False
    if 'selected_choice' in st.session_state:
        del st.session_state.selected_choice

def get_final_grade():
    """Calculate final grade based on remaining money"""
    money = st.session_state.game_state['money']
    if money > 300000:
        return "A+", "🏆 Suraksha Master!", "Excellent! You're a true insurance champion!", "#4CAF50"
    elif money > 150000:
        return "B+", "👍 Samjhdar Player!", "Good job! You made mostly smart decisions.", "#FF9800"
    elif money > 50000:
        return "C", "😐 Theek Hai", "You survived, but need better planning.", "#FFC107"
    elif money > 0:
        return "D", "😰 Mushkil Mein", "Financial stress! Better insurance needed.", "#FF5722"
    else:
        return "F", "💸 Tabahi!", "Complete financial disaster! Start over.", "#F44336"

# Main App
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ सुरक्षा शक्ति (Suraksha Shakti)</h1>
        <h3>Indian Insurance Decision Game</h3>
        <p style="font-size: 1.2rem; margin-top: 1rem;">
            Make smart insurance choices and protect your family's future!<br>
            <span class="hindi-text">बुद्धिमानी से बीमा चुनें और अपने परिवार का भविष्य सुरक्षित करें!</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Game not started
    if not st.session_state.game_state['game_started']:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            ### 🎮 How to Play:
            - You start with ₹5 lakh savings
            - Face 4 real-life scenarios every Indian family encounters
            - Choose insurance policies wisely
            - Random events will test your decisions
            - Protect your money and your family!
            
            ### गेम कैसे खेलें:
            - आप ₹5 लाख बचत के साथ शुरुआत करते हैं
            - 4 वास्तविक जीवन स्थितियों का सामना करें
            - समझदारी से बीमा पॉलिसी चुनें
            - आपके फैसलों की परीक्षा होगी
            """)
            
            if st.button("🚀 Start Game / गेम शुरू करें", type="primary", use_container_width=True):
                st.session_state.game_state['game_started'] = True
                st.rerun()
        return

    # Game Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stats-container">
            <h3 style="text-align: center; margin-bottom: 0.5rem;">💰 Savings</h3>
            <h2 style="text-align: center; color: #4CAF50; margin: 0;">{format_currency(st.session_state.game_state['money'])}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-container">
            <h3 style="text-align: center; margin-bottom: 0.5rem;">🛡️ Coverage</h3>
            <h2 style="text-align: center; color: #2196F3; margin: 0;">{format_currency(st.session_state.game_state['coverage'])}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-container">
            <h3 style="text-align: center; margin-bottom: 0.5rem;">📊 Scenario</h3>
            <h2 style="text-align: center; color: #FF9800; margin: 0;">{st.session_state.game_state['current_scenario'] + 1}/4</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        progress = (st.session_state.game_state['current_scenario'] / len(scenarios)) * 100
        st.markdown(f"""
        <div class="stats-container">
            <h3 style="text-align: center; margin-bottom: 0.5rem;">⏱️ Progress</h3>
            <div style="background: #E0E0E0; border-radius: 10px; height: 20px; margin-top: 10px;">
                <div style="background: linear-gradient(90deg, #4CAF50, #8BC34A); height: 100%; width: {progress}%; border-radius: 10px; transition: width 0.3s ease;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Check if game is complete
    if st.session_state.game_state['current_scenario'] >= len(scenarios):
        grade, title, message, color = get_final_grade()
        
        st.markdown(f"""
        <div class="scenario-card" style="text-align: center;">
            <h2>🎯 Game Complete! / खेल समाप्त!</h2>
            <div class="final-grade" style="color: {color};">{grade}</div>
            <h3>{title}</h3>
            <p style="font-size: 1.3rem; margin: 1.5rem 0;">{message}</p>
            
            <div style="background: #F5F5F5; padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0;">
                <h4>📈 Final Results:</h4>
                <p><strong>Money Left:</strong> {format_currency(st.session_state.game_state['money'])}</p>
                <p><strong>Total Coverage:</strong> {format_currency(st.session_state.game_state['coverage'])}</p>
                <p><strong>Insurance Types:</strong> {len([t for t in st.session_state.game_state['insurance_types'] if t != 'none'])}/4</p>
            </div>
            
            <p style="color: #666; font-size: 1.1rem;">
                Insurance sikhaya hai ki planning zaroori hai!<br>
                <em>बीमा ने सिखाया है कि योजना बनाना जरूरी है!</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Play Again / फिर से खेलें", type="primary", use_container_width=True):
                reset_game()
                st.rerun()
        return

    # Current scenario
    scenario = scenarios[st.session_state.game_state['current_scenario']]
    
    st.markdown(f"""
    <div class="scenario-card">
        <h2>{scenario['title']}</h2>
        <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 1rem;">{scenario['text']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Show choices if not made yet
    if not st.session_state.game_state['choice_made']:
        st.markdown("### Choose Your Insurance Strategy:")
        
        for i, choice in enumerate(scenario['choices']):
            if st.button(
                f"**{choice['title']}**\n\n{choice['description']}\n\n_{choice['hindi']}_",
                key=f"choice_{i}",
                use_container_width=True
            ):
                make_choice(i)
                st.rerun()
    
    # Show choice result and event
    elif st.session_state.game_state['choice_made']:
        choice = st.session_state.selected_choice
        
        # Show choice confirmation
        st.markdown(f"""
        <div class="result-good">
            <h3>✅ Decision Made! / फैसला हो गया!</h3>
            <p><strong>You chose:</strong> {choice['title']}</p>
            <p><strong>Cost:</strong> {format_currency(choice['cost'])} per year</p>
            <p><strong>Coverage Added:</strong> {format_currency(choice['coverage'])}</p>
            <p style="margin-top: 1rem; font-style: italic;">{choice['hindi']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show event immediately if not shown yet
        if not st.session_state.game_state['event_shown']:
            # Add a small delay for better UX
            with st.spinner("देखते हैं क्या होता है... / Let's see what happens..."):
                time.sleep(1)
            
            # Show the event
            event, covered, out_of_pocket = show_event()
            
            result_class = "result-good" if out_of_pocket == 0 else "result-bad"
            
            st.markdown(f"""
            <div class="{result_class}">
                <h3>{event['title']}</h3>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">{event['description']}</p>
                <p><em>{event['hindi']}</em></p>
                
                <hr style="margin: 1rem 0;">
                
                <p><strong>💸 Total Cost:</strong> {format_currency(event['damage'])}</p>
                <p><strong>🛡️ Insurance Covered:</strong> {format_currency(covered)}</p>
                <p><strong>💰 You Pay:</strong> {format_currency(out_of_pocket)}</p>
                
                {"<p><strong>🎉 Fully covered by insurance! / बीमा ने पूरा कवर किया!</strong></p>" if out_of_pocket == 0 else ""}
                {"<p><strong>💸 This is a major financial hit! / यह बड़ा नुकसान है!</strong></p>" if out_of_pocket > 200000 else ""}
            </div>
            """, unsafe_allow_html=True)
            
            # Show next button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("➡️ Next Scenario / अगली स्थिति", type="primary", use_container_width=True):
                    next_scenario()
                    st.rerun()

    # Restart button in sidebar
    with st.sidebar:
        st.markdown("### Game Controls")
        if st.button("🔄 Restart Game", type="secondary"):
            reset_game()
            st.rerun()
        
        st.markdown("### Insurance Tips")
        st.info("""
        💡 **Smart Tips:**
        - Health insurance is most important
        - Term life insurance is cheapest 
        - Don't skip vehicle insurance
        - Compare coverage vs. cost
        
        **स्मार्ट टिप्स:**
        - स्वास्थ्य बीमा सबसे जरूरी
        - टर्म जीवन बीमा सबसे सस्ता
        - वाहन बीमा न छोड़ें
        """)

if __name__ == "__main__":
    main()
