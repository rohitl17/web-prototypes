import random
import streamlit as st
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import pandas as pd

st.set_page_config(
    page_title="Knowledge Arcade — Quiz Arena",
    page_icon="🎯",
    layout="wide",
)


QUIZ_DOMAINS: Dict[str, Dict] = {
    "data_ai": {
        "title": "Data & AI",
        "emoji": "🤖",
        "description": "Modeling best practices, evaluation metrics, and responsible AI.",
        "questions": [
            {
                "q": "Which regularization technique adds the absolute value of coefficients to the loss function?",
                "options": [
                    "L1 regularization (Lasso)",
                    "L2 regularization (Ridge)",
                    "Dropout",
                ],
                "answer": 0,
            },
            {
                "q": "What does the ROC curve plot?",
                "options": [
                    "True positive rate vs. false positive rate",
                    "Precision vs. recall",
                    "Accuracy vs. epochs",
                ],
                "answer": 0,
            },
            {
                "q": "Which optimizer adapts individual learning rates using first and second moments of gradients?",
                "options": ["SGD", "Adam", "RMSprop"],
                "answer": 1,
            },
            {
                "q": "Dropout during training is primarily used to:",
                "options": [
                    "Reduce co-adaptation and improve generalization",
                    "Accelerate GPU throughput",
                    "Increase model depth",
                ],
                "answer": 0,
            },
            {
                "q": "Which technique is commonly applied to address class imbalance?",
                "options": ["SMOTE", "Batch normalization", "Label smoothing"],
                "answer": 0,
            },
            {
                "q": "Why is feature scaling important for gradient-based models?",
                "options": [
                    "It ensures features contribute comparably to weight updates",
                    "It guarantees loss reaches zero",
                    "It doubles the number of features",
                ],
                "answer": 0,
            },
            {
                "q": "Precision is defined as:",
                "options": [
                    "TP / (TP + FP)",
                    "TP / (TP + FN)",
                    "TN / (TN + FP)",
                ],
                "answer": 0,
            },
            {
                "q": "Which hyperparameter search method builds a surrogate model of the objective to pick the next trial?",
                "options": [
                    "Bayesian optimization",
                    "Mini-batch gradient descent",
                    "Early stopping",
                ],
                "answer": 0,
            },
            {
                "q": "Cross-validation primarily helps with:",
                "options": [
                    "Estimating how well the model generalizes to unseen data",
                    "Increasing the number of training epochs",
                    "Adding more features automatically",
                ],
                "answer": 0,
            },
            {
                "q": "A core pillar of responsible AI that ensures models do not disproportionately harm subgroups is called:",
                "options": ["Fairness", "Latency", "Throughput"],
                "answer": 0,
            },
            {
                "q": "K-means clustering implicitly assumes:",
                "options": [
                    "Clusters are roughly spherical and similarly sized",
                    "Clusters follow arbitrary shapes",
                    "Each cluster contains only one sample",
                ],
                "answer": 0,
            },
            {
                "q": "Within a confusion matrix, false negatives count:",
                "options": [
                    "Positive cases the model predicted as negative",
                    "Negative cases the model predicted as positive",
                    "True negatives",
                ],
                "answer": 0,
            },
        ],
    },
    "business_strategy": {
        "title": "Business Strategy",
        "emoji": "📈",
        "description": "Frameworks, metrics, and operating models leaders rely on.",
        "questions": [
            {
                "q": "SWOT analysis evaluates strengths, weaknesses, opportunities, and:",
                "options": ["Threats", "Targets", "Timelines"],
                "answer": 0,
            },
            {
                "q": "Which perspective is part of the Balanced Scorecard?",
                "options": [
                    "Learning and growth",
                    "Vendor compliance",
                    "Share price",
                ],
                "answer": 0,
            },
            {
                "q": "Blue Ocean Strategy primarily aims to:",
                "options": [
                    "Create uncontested market space through value innovation",
                    "Compete head-to-head on price",
                    "Focus solely on cost cutting",
                ],
                "answer": 0,
            },
            {
                "q": "Key Performance Indicators differ from general metrics because they:",
                "options": [
                    "Tie directly to strategic objectives",
                    "Are always financial",
                    "Only track daily operations",
                ],
                "answer": 0,
            },
            {
                "q": "Net Present Value (NPV) measures:",
                "options": [
                    "The value today of future cash flows discounted at a chosen rate",
                    "The total revenue across a product's lifetime",
                    "Inventory carrying cost per unit",
                ],
                "answer": 0,
            },
            {
                "q": "Porter's Five Forces framework analyzes:",
                "options": [
                    "Industry attractiveness and competitive pressure",
                    "Internal supply chain efficiency",
                    "Employee engagement levels",
                ],
                "answer": 0,
            },
            {
                "q": "The break-even point represents the sales level where:",
                "options": [
                    "Total revenue equals total costs",
                    "Gross margin hits 50%",
                    "Marketing spend can be reduced",
                ],
                "answer": 0,
            },
            {
                "q": "In SMART goals, the letter T refers to:",
                "options": ["Time-bound", "Transparent", "Tailored"],
                "answer": 0,
            },
            {
                "q": "A compelling value proposition describes:",
                "options": [
                    "The unique benefit your offering delivers to the target customer",
                    "An internal budget approval",
                    "The size of your org chart",
                ],
                "answer": 0,
            },
            {
                "q": "Vertical integration occurs when a company:",
                "options": [
                    "Expands to control additional stages of its supply chain",
                    "Outsources manufacturing",
                    "Focuses solely on franchising",
                ],
                "answer": 0,
            },
            {
                "q": "Economies of scale mean that:",
                "options": [
                    "Unit costs decrease as production volume increases",
                    "Marketing spend must double each year",
                    "Only large firms can innovate",
                ],
                "answer": 0,
            },
            {
                "q": "Which of the following is a leading indicator of strategy execution?",
                "options": [
                    "Pipeline of qualified prospects",
                    "Last quarter's revenue",
                    "Tax rate from last year",
                ],
                "answer": 0,
            },
        ],
    },
    "communication": {
        "title": "Communication",
        "emoji": "💬",
        "description": "Messaging clarity, stakeholder updates, and active listening skills.",
        "questions": [
            {
                "q": "Active listening often involves:",
                "options": [
                    "Paraphrasing to confirm understanding",
                    "Waiting to interrupt",
                    "Multitasking while someone speaks",
                ],
                "answer": 0,
            },
            {
                "q": "Which channel best preserves nuance for complex decisions?",
                "options": ["Video or in-person conversation", "Instant message", "Emoji reaction"],
                "answer": 0,
            },
            {
                "q": "The SBI model for feedback stands for:",
                "options": [
                    "Situation, Behavior, Impact",
                    "Signal, Body, Intent",
                    "Summary, Benefit, Indicator",
                ],
                "answer": 0,
            },
            {
                "q": "An assertive communication style is best characterized by:",
                "options": [
                    "Clear, respectful expression of needs",
                    "Avoiding direct statements",
                    "Dominating every conversation",
                ],
                "answer": 0,
            },
            {
                "q": "Open-ended questions are useful when you want to:",
                "options": [
                    "Encourage elaboration and deeper insight",
                    "Receive a yes/no answer quickly",
                    "Close a discussion",
                ],
                "answer": 0,
            },
            {
                "q": "Which element is essential in an executive-ready update?",
                "options": [
                    "Upfront summary of status, risk, and ask",
                    "Chronological detail of every task",
                    "Only technical jargon",
                ],
                "answer": 0,
            },
            {
                "q": "Non-verbal cues such as posture and eye contact primarily reinforce:",
                "options": [
                    "Credibility and engagement",
                    "Slide typography",
                    "Meeting length",
                ],
                "answer": 0,
            },
            {
                "q": "When preparing a communication plan you should define:",
                "options": [
                    "Audience, message, channel, and cadence",
                    "Only the font size",
                    "Exact script for improvised Q&A",
                ],
                "answer": 0,
            },
            {
                "q": "Empathetic statements typically:",
                "options": [
                    "Acknowledge the other person's perspective",
                    "Deflect responsibility",
                    "Shift blame immediately",
                ],
                "answer": 0,
            },
            {
                "q": "Storytelling in business communication helps because:",
                "options": [
                    "Narratives make data memorable and relatable",
                    "It replaces the need for metrics",
                    "It shortens every meeting",
                ],
                "answer": 0,
            },
            {
                "q": "Which technique improves async written updates?",
                "options": [
                    "Use headings and TL;DR sections for scannability",
                    "Hide key decisions in paragraphs",
                    "Rely on acronyms only",
                ],
                "answer": 0,
            },
            {
                "q": "The best follow-up to a difficult conversation is to:",
                "options": [
                    "Summarize agreements and next steps in writing",
                    "Avoid the person for weeks",
                    "Ask someone else to guess what was decided",
                ],
                "answer": 0,
            },
        ],
    },
    "sales_marketing": {
        "title": "Sales & Marketing",
        "emoji": "📣",
        "description": "Pipeline math, campaign tactics, and customer metrics.",
        "questions": [
            {
                "q": "Conversion rate is calculated as:",
                "options": [
                    "Number of conversions divided by total visitors",
                    "Total spend divided by impressions",
                    "Qualified leads times win rate",
                ],
                "answer": 0,
            },
            {
                "q": "A call-to-action (CTA) should be:",
                "options": [
                    "Clear, specific, and action-oriented",
                    "Hidden at the bottom of long text",
                    "Used once per quarter",
                ],
                "answer": 0,
            },
            {
                "q": "Lead scoring helps teams:",
                "options": [
                    "Prioritize prospects most likely to convert",
                    "Set employee bonuses",
                    "Pick event venues",
                ],
                "answer": 0,
            },
            {
                "q": "CRM platforms are primarily used to:",
                "options": [
                    "Track customer interactions and deal stages",
                    "Design product packaging",
                    "Manage payroll",
                ],
                "answer": 0,
            },
            {
                "q": "A/B testing in marketing allows teams to:",
                "options": [
                    "Compare performance of two variants with statistical rigor",
                    "Track inventory levels",
                    "Eliminate campaign budgets",
                ],
                "answer": 0,
            },
            {
                "q": "Pay-per-click (PPC) campaigns charge advertisers:",
                "options": [
                    "Each time a user clicks on their ad",
                    "One fee per creative asset",
                    "Monthly regardless of engagement",
                ],
                "answer": 0,
            },
            {
                "q": "Which funnel stage focuses on nurturing interest into intent?",
                "options": [
                    "Middle of the funnel",
                    "Top of the funnel",
                    "Post-purchase",
                ],
                "answer": 0,
            },
            {
                "q": "Customer lifetime value (CLV) estimates:",
                "options": [
                    "Total net revenue expected from a customer over the relationship",
                    "Annual support ticket volume",
                    "Cost per acquisition",
                ],
                "answer": 0,
            },
            {
                "q": "STP in marketing stands for:",
                "options": [
                    "Segmentation, Targeting, Positioning",
                    "Sell, Test, Promote",
                    "Spend, Track, Profit",
                ],
                "answer": 0,
            },
            {
                "q": "Content marketing aims to:",
                "options": [
                    "Provide helpful information that earns trust and drives action",
                    "Replace product onboarding",
                    "Lower support headcount",
                ],
                "answer": 0,
            },
            {
                "q": "Net Promoter Score (NPS) asks customers to:",
                "options": [
                    "Rate how likely they are to recommend the product",
                    "List every feature they dislike",
                    "Reveal total budget",
                ],
                "answer": 0,
            },
            {
                "q": "Multitouch attribution models help teams understand:",
                "options": [
                    "How different interactions contribute to a final conversion",
                    "Which salesperson is tallest",
                    "Exact manufacturing cost",
                ],
                "answer": 0,
            },
        ],
    },
    "product_management": {
        "title": "Product Management",
        "emoji": "🧭",
        "description": "Roadmapping, discovery, and measuring product outcomes.",
        "questions": [
            {
                "q": "A minimum viable product (MVP) is best described as:",
                "options": [
                    "The smallest experiment that delivers value and validates hypotheses",
                    "A throwaway prototype only engineers see",
                    "The full roadmap for three years",
                ],
                "answer": 0,
            },
            {
                "q": "The RICE framework prioritizes work using:",
                "options": [
                    "Reach, Impact, Confidence, Effort",
                    "Revenue, Iteration, Cost, Efficiency",
                    "Risk, Innovation, Cost, Enablement",
                ],
                "answer": 0,
            },
            {
                "q": "Product discovery focuses on:",
                "options": [
                    "Understanding user problems before committing to solutions",
                    "Locking the release date",
                    "Scaling infrastructure",
                ],
                "answer": 0,
            },
            {
                "q": "Objectives and Key Results (OKRs) help teams:",
                "options": [
                    "Align around outcomes rather than output",
                    "Replace daily standups",
                    "Eliminate stakeholder reviews",
                ],
                "answer": 0,
            },
            {
                "q": "Backlog refinement (grooming) is used to:",
                "options": [
                    "Clarify, estimate, and reorder upcoming work",
                    "Remove testing tasks",
                    "Finalize contracts",
                ],
                "answer": 0,
            },
            {
                "q": "Feature flags are helpful because they:",
                "options": [
                    "Allow gradual rollouts and quick rollbacks",
                    "Increase build size",
                    "Replace documentation",
                ],
                "answer": 0,
            },
            {
                "q": "A North Star metric should:",
                "options": [
                    "Represent the long-term value delivered to users",
                    "Track code commits",
                    "Equal revenue growth every month",
                ],
                "answer": 0,
            },
            {
                "q": "Which prioritization method scores work by customer value vs. implementation effort?",
                "options": [
                    "Impact vs. effort matrix",
                    "Monte Carlo simulation",
                    "Earned value analysis",
                ],
                "answer": 0,
            },
            {
                "q": "Jobs-to-be-Done (JTBD) framing centers on:",
                "options": [
                    "The progress customers seek in specific situations",
                    "Listing every feature request",
                    "Measuring sprint velocity",
                ],
                "answer": 0,
            },
            {
                "q": "Product/market fit is indicated when:",
                "options": [
                    "A clearly defined market repeatedly pulls the product with minimal marketing push",
                    "The backlog has 100 items",
                    "Revenue equals costs",
                ],
                "answer": 0,
            },
            {
                "q": "Cohort retention analysis helps teams understand:",
                "options": [
                    "How user groups behave over time after activation",
                    "Which engineer fixed the most bugs",
                    "The required QA headcount",
                ],
                "answer": 0,
            },
            {
                "q": "A launch readiness checklist typically includes:",
                "options": [
                    "Support playbooks, analytics hooks, and go-to-market alignment",
                    "Hiring plans for next year",
                    "GDP growth by country",
                ],
                "answer": 0,
            },
        ],
    },
    "general_knowledge": {
        "title": "General Knowledge",
        "emoji": "🌍",
        "description": "Science, history, geography, and culture tidbits.",
        "questions": [
            {
                "q": "Which planet is known as the Red Planet?",
                "options": ["Mars", "Venus", "Mercury"],
                "answer": 0,
            },
            {
                "q": "The process by which plants make food using sunlight is called:",
                "options": ["Photosynthesis", "Respiration", "Fermentation"],
                "answer": 0,
            },
            {
                "q": "Which ocean is the largest on Earth?",
                "options": ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean"],
                "answer": 0,
            },
            {
                "q": "Who wrote the play 'Romeo and Juliet'?",
                "options": ["William Shakespeare", "Charles Dickens", "Jane Austen"],
                "answer": 0,
            },
            {
                "q": "Fe is the chemical symbol for:",
                "options": ["Iron", "Fluorine", "Francium"],
                "answer": 0,
            },
            {
                "q": "Which scientist proposed the theory of general relativity?",
                "options": ["Albert Einstein", "Isaac Newton", "Niels Bohr"],
                "answer": 0,
            },
            {
                "q": "What is the capital of Japan?",
                "options": ["Tokyo", "Osaka", "Kyoto"],
                "answer": 0,
            },
            {
                "q": "In computing, 'HTTP' stands for:",
                "options": [
                    "HyperText Transfer Protocol",
                    "High Tech Transit Process",
                    "Hybrid Transmission Pipeline",
                ],
                "answer": 0,
            },
            {
                "q": "Which organ in the human body is primarily responsible for detoxification?",
                "options": ["Liver", "Heart", "Spleen"],
                "answer": 0,
            },
            {
                "q": "The longest river in the world is commonly considered to be the:",
                "options": ["Nile River", "Amazon River", "Yangtze River"],
                "answer": 0,
            },
            {
                "q": "Which artist painted the Mona Lisa?",
                "options": ["Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso"],
                "answer": 0,
            },
            {
                "q": "Which gas is most abundant in Earth's atmosphere?",
                "options": ["Nitrogen", "Oxygen", "Carbon dioxide"],
                "answer": 0,
            },
        ],
    },
}

LEADERBOARD_PATH = Path(__file__).with_name("leaderboard.csv")
LEADERBOARD_COLUMNS = ["timestamp", "player", "domain", "score", "total", "percent"]


def load_leaderboard() -> pd.DataFrame:
    if LEADERBOARD_PATH.exists():
        return pd.read_csv(LEADERBOARD_PATH)
    return pd.DataFrame(columns=LEADERBOARD_COLUMNS)


def record_score(player: str, domain: str, score: int, total: int) -> None:
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "player": player or "Anonymous",
        "domain": domain,
        "score": score,
        "total": total,
        "percent": round((score / total) * 100, 1),
    }
    leaderboard = load_leaderboard()
    leaderboard = pd.concat([leaderboard, pd.DataFrame([entry])], ignore_index=True)
    leaderboard.to_csv(LEADERBOARD_PATH, index=False)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            .hero-container {
                background: radial-gradient(circle at top left, #2e236c, #150f3e 55%, #09091f);
                border-radius: 24px;
                padding: 2.5rem 3rem;
                color: #f8fafc;
                margin-bottom: 2rem;
                box-shadow: 0 18px 45px rgba(3, 7, 18, 0.55);
            }
            .hero-heading {
                font-size: 2.4rem;
                font-weight: 700;
                margin-bottom: 0.4rem;
            }
            .hero-sub {
                font-size: 1.1rem;
                opacity: 0.85;
            }
            .highlight-pill {
                display: inline-block;
                border-radius: 999px;
                padding: 0.35rem 1rem;
                background: rgba(248, 250, 252, 0.15);
                margin-bottom: 0.8rem;
                font-size: 0.85rem;
                letter-spacing: 0.05em;
            }
            .domain-card {
                border-radius: 18px;
                padding: 1.5rem;
                background: #ffffff;
                border: 1px solid rgba(148, 163, 184, 0.35);
                box-shadow: 0 10px 20px rgba(15, 23, 42, 0.08);
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            .domain-card:hover {
                border-color: #6366f1;
                box-shadow: 0 18px 32px rgba(99, 102, 241, 0.25);
            }
            .domain-emoji {
                font-size: 2.3rem;
                margin-bottom: 0.5rem;
            }
            .domain-meta {
                font-size: 0.9rem;
                color: #475569;
            }
            .feature-card {
                border-radius: 16px;
                padding: 1.25rem;
                background: rgba(255, 255, 255, 0.6);
                border: 1px solid rgba(148, 163, 184, 0.3);
                backdrop-filter: blur(4px);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state() -> None:
    st.session_state.setdefault("phase", "landing")
    st.session_state.setdefault("domain_key", None)
    st.session_state.setdefault("current_question", 0)
    st.session_state.setdefault("answers", [])
    st.session_state.setdefault("player_name", "")
    st.session_state.setdefault("leaderboard_saved", False)
    st.session_state.setdefault("active_questions", [])


def reset_quiz() -> None:
    st.session_state.phase = "landing"
    st.session_state.domain_key = None
    st.session_state.current_question = 0
    st.session_state.answers = []
    st.session_state.leaderboard_saved = False
    st.session_state.active_questions = []


def start_quiz(domain_key: str) -> None:
    question_pool = QUIZ_DOMAINS[domain_key]["questions"]
    sample_size = min(10, len(question_pool))
    st.session_state.phase = "quiz"
    st.session_state.domain_key = domain_key
    st.session_state.current_question = 0
    st.session_state.active_questions = random.sample(question_pool, sample_size)
    st.session_state.answers = [None] * sample_size
    st.session_state.leaderboard_saved = False


def landing_page() -> None:
    total_questions = sum(len(domain["questions"]) for domain in QUIZ_DOMAINS.values())
    leaderboard = load_leaderboard()

    st.markdown(
        """
        <div class="hero-container">
            <div class="highlight-pill">NEW • Multiplayer quiz hub</div>
            <div class="hero-heading">Knowledge Arcade</div>
            <div class="hero-sub">
                Explore business, communication, product, and data domains. Each run serves 10 random questions, so no two sessions feel the same—even when hundreds of players jump in simultaneously.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    stats_cols = st.columns(4)
    stats_cols[0].metric("Quiz domains", len(QUIZ_DOMAINS))
    stats_cols[1].metric("Questions in bank", total_questions)
    stats_cols[2].metric("Leaderboard entries", len(leaderboard))
    stats_cols[3].metric("Questions per run", 10)

    feature_cols = st.columns(3)
    feature_cols[0].markdown(
        "<div class='feature-card'><strong>Configurable pools</strong><br/>Admins can expand any category just by editing the dictionary.</div>",
        unsafe_allow_html=True,
    )
    feature_cols[1].markdown(
        "<div class='feature-card'><strong>Massively scalable</strong><br/>Each browser tab keeps its own state, so hundreds can play in parallel.</div>",
        unsafe_allow_html=True,
    )
    feature_cols[2].markdown(
        "<div class='feature-card'><strong>Global leaderboard</strong><br/>Log your score and challenge your peers instantly.</div>",
        unsafe_allow_html=True,
    )

    name = st.text_input(
        "Display name (for leaderboard)",
        value=st.session_state.player_name,
        placeholder="Add your name or keep it blank",
    )
    st.session_state.player_name = name.strip()

    st.caption("Select a category to receive 10 random questions from its bank.")
    domain_items = list(QUIZ_DOMAINS.items())
    num_cols = min(3, max(1, len(domain_items)))
    for i in range(0, len(domain_items), num_cols):
        cols = st.columns(num_cols)
        for col, (domain_key, domain) in zip(cols, domain_items[i : i + num_cols]):
            with col:
                st.markdown(
                    f"""
                    <div class="domain-card">
                        <div>
                            <div class="domain-emoji">{domain.get('emoji', '🎯')}</div>
                            <h3>{domain['title']}</h3>
                            <p>{domain['description']}</p>
                        </div>
                        <p class="domain-meta">{len(domain['questions'])} questions in bank · 10 served per run</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.button(
                    f"Play {domain['title']}",
                    key=f"start_{domain_key}",
                    use_container_width=True,
                    on_click=start_quiz,
                    args=(domain_key,),
                )

    with st.expander("View global leaderboard (top 10)"):
        if leaderboard.empty:
            st.info("No entries yet. Be the first one to post a score!")
        else:
            top = leaderboard.sort_values(
                by=["percent", "timestamp"], ascending=[False, False]
            ).head(10)
            display_cols = ["player", "domain", "score", "total", "percent", "timestamp"]
            st.table(top[display_cols])


def quiz_page() -> None:
    domain_key = st.session_state.domain_key
    if not domain_key:
        st.warning("Pick a domain first.")
        reset_quiz()
        return

    questions = st.session_state.active_questions
    if not questions:
        start_quiz(domain_key)
        questions = st.session_state.active_questions

    domain = QUIZ_DOMAINS[domain_key]
    idx = st.session_state.current_question
    current = questions[idx]
    total = len(questions)

    st.sidebar.header("Quiz Controls")
    if st.session_state.player_name:
        st.sidebar.write(f"Player: **{st.session_state.player_name}**")
    st.sidebar.write(f"Domain: **{domain['title']}**")
    st.sidebar.progress((idx + 1) / total)
    st.sidebar.write(f"Question {idx + 1} of {total}")
    st.sidebar.button("Return to title", on_click=reset_quiz)

    st.title(f"{domain.get('emoji', '🎯')} {domain['title']}")
    st.subheader(f"Question {idx + 1}")
    st.write(current["q"])

    answer_idx = st.session_state.answers[idx]
    choice = st.radio(
        "Select an answer",
        options=list(range(len(current["options"]))),
        format_func=lambda option_index: current["options"][option_index],
        index=answer_idx if answer_idx is not None else 0,
        key=f"radio_{domain_key}_{idx}",
    )
    st.session_state.answers[idx] = choice

    col1, col2, col3 = st.columns(3)
    with col1:
        st.button(
            "Previous",
            disabled=idx == 0,
            on_click=lambda: st.session_state.update(current_question=idx - 1),
        )
    with col3:
        st.button(
            "Next",
            disabled=idx == total - 1,
            on_click=lambda: st.session_state.update(current_question=idx + 1),
        )
    with col2:
        if st.button("Submit quiz", disabled=None in st.session_state.answers):
            st.session_state.phase = "results"


def results_page() -> None:
    domain_key = st.session_state.domain_key
    if not domain_key:
        st.warning("Select a domain first.")
        reset_quiz()
        return

    questions = st.session_state.active_questions
    answers = st.session_state.answers

    score = 0
    rows: List[Dict] = []
    for idx, q in enumerate(questions):
        selected = answers[idx]
        correct = q["answer"]
        is_correct = selected == correct
        if is_correct:
            score += 1
        rows.append(
            {
                "Q#": idx + 1,
                "Question": q["q"],
                "Your answer": q["options"][selected] if selected is not None else "(no answer)",
                "Correct": q["options"][correct],
                "Correct?": "Yes" if is_correct else "No",
            }
        )

    domain = QUIZ_DOMAINS[domain_key]
    st.title("Quiz Results")
    st.subheader(domain["title"])
    st.metric("Score", f"{score} / {len(questions)}")
    df = pd.DataFrame(rows).set_index("Q#")
    st.table(df)

    st.success("Great work! Replay to get a new random mix or log your score.")

    leaderboard = load_leaderboard()
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Replay domain"):
            start_quiz(domain_key)
    with col2:
        if st.button("Choose another domain"):
            reset_quiz()
    with col3:
        saved = st.session_state.leaderboard_saved
        if st.button(
            "Save to leaderboard",
            disabled=saved,
            use_container_width=True,
        ):
            record_score(
                st.session_state.player_name,
                domain["title"],
                score,
                len(questions),
            )
            st.session_state.leaderboard_saved = True
            leaderboard = load_leaderboard()
            st.success("Score posted to the leaderboard!", icon="✅")
        if saved:
            st.caption("Already posted ✅")

    with st.expander("Leaderboard highlights"):
        if leaderboard.empty:
            st.info("No leaderboard entries yet.")
        else:
            top = leaderboard.sort_values(
                by=["percent", "timestamp"], ascending=[False, False]
            ).head(10)
            display_cols = ["player", "domain", "score", "total", "percent", "timestamp"]
            st.table(top[display_cols])


def main() -> None:
    init_state()
    inject_styles()

    phase = st.session_state.phase
    if phase == "landing":
        landing_page()
    elif phase == "quiz":
        quiz_page()
    elif phase == "results":
        results_page()


if __name__ == "__main__":
    main()
