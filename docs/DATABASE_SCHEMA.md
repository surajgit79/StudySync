# StudySync - Database Schema Documentation

## Database: MongoDB

MongoDB was chosen for its flexibility with nested documents, scalability, and excellent performance with complex queries involving embedded data structures.

## Collections Overview

1. **users** - Student profiles and authentication
2. **study_groups** - Study group information
3. **study_sessions** - Individual study session records
4. **learning_patterns** - Daily learning activity data
5. **recommendations** - Generated recommendations and user feedback
6. **achievements** - Achievement definitions
7. **messages** - Chat messages
8. **notifications** - User notifications
9. **partner_requests** - Study partner connection requests
10. **group_memberships** - Group membership history
11. **analytics_cache** - Cached analytics results

## Detailed Collection Schemas

### 1. users Collection

Stores user authentication and profile information.

```javascript
{
  _id: ObjectId("..."),

  // Authentication
  email: "student@university.edu",
  username: "johndoe",
  password_hash: "bcrypt_hashed_password",
  is_active: true,
  is_verified: false,
  email_verification_token: "token_string",
  password_reset_token: null,

  // Profile Information
  profile: {
    full_name: "John Doe",
    avatar_url: "https://...",
    institution: "MIT",
    major: "Computer Science",
    year: 3,
    gpa: 3.7,

    // Learning Preferences
    learning_pace: "moderate",  // fast, moderate, slow
    learning_style: ["visual", "kinesthetic"],
    study_goals: [
      {
        subject: "Machine Learning",
        target_grade: "A",
        deadline: ISODate("2024-05-15"),
        priority: "high"
      }
    ],

    // Availability
    study_schedule: {
      monday: [
        { start: "14:00", end: "17:00" },
        { start: "19:00", end: "21:00" }
      ],
      tuesday: [{ start: "15:00", end: "18:00" }],
      // ... other days
    },
    timezone: "America/New_York",

    // Skills & Interests
    skills: [
      {
        name: "Python Programming",
        level: "advanced",  // beginner, intermediate, advanced, expert
        verified: true
      },
      {
        name: "Data Structures",
        level: "intermediate",
        verified: false
      }
    ],
    subjects_of_interest: ["AI", "Machine Learning", "Algorithms"],

    // Preferences
    preferred_group_size: 4,
    open_to_teaching: true,
    seeking_help_with: ["Calculus", "Physics"],

    // Bio
    bio: "CS student passionate about AI...",
    languages: ["English", "Spanish"]
  },

  // Gamification Data
  gamification: {
    points: 1250,
    level: 8,
    experience: 350,  // XP toward next level
    experience_to_next_level: 500,
    badges: [
      ObjectId("achievement_id_1"),
      ObjectId("achievement_id_2")
    ],
    achievements_unlocked: [
      {
        achievement_id: ObjectId("..."),
        unlocked_at: ISODate("2024-01-15T10:30:00Z"),
        progress: 100
      }
    ],
    streaks: {
      current_study_streak: 7,  // days
      longest_study_streak: 23,
      current_login_streak: 12,
      longest_login_streak: 45,
      last_activity_date: ISODate("2024-01-20")
    },
    statistics: {
      total_study_hours: 156,
      groups_joined: 5,
      partners_connected: 12,
      sessions_completed: 89,
      resources_shared: 34,
      helped_peers: 23
    }
  },

  // ML/Analytics Data
  ml_data: {
    cluster_label: 2,  // From K-Means clustering
    cluster_assigned_at: ISODate("2024-01-15"),
    learning_pattern_type: "night_owl",
    productivity_score: 7.8,
    collaboration_success_rate: 0.85,
    compatibility_vector: [0.7, 0.8, 0.6, 0.9, 0.75],  // For similarity matching
    last_model_update: ISODate("2024-01-20")
  },

  // Preferences & Settings
  settings: {
    email_notifications: true,
    push_notifications: true,
    privacy_level: "friends_only",  // public, friends_only, private
    show_in_search: true,
    allow_partner_requests: true,
    theme: "light"  // light, dark, auto
  },

  // Metadata
  created_at: ISODate("2024-01-01T12:00:00Z"),
  updated_at: ISODate("2024-01-20T15:30:00Z"),
  last_login: ISODate("2024-01-20T15:30:00Z"),
  last_active: ISODate("2024-01-20T18:45:00Z"),

  // Status
  status: "active",  // active, inactive, suspended, deleted

  // Indexes needed
  indexes: [
    { email: 1 },  // unique
    { username: 1 },  // unique
    { "profile.institution": 1, "profile.major": 1 },
    { "ml_data.cluster_label": 1 },
    { "gamification.points": -1 },
    { created_at: -1 }
  ]
}
```

### 2. study_groups Collection

Stores study group information and metrics.

```javascript
{
  _id: ObjectId("..."),

  // Basic Information
  name: "Advanced ML Study Group",
  description: "Graduate students studying ML together",
  subject: "Machine Learning",
  tags: ["ML", "AI", "Graduate", "Advanced"],

  // Members
  creator_id: ObjectId("user_id"),
  members: [
    {
      user_id: ObjectId("user_id_1"),
      role: "admin",  // admin, moderator, member
      joined_at: ISODate("2024-01-01"),
      contribution_score: 85,
      is_active: true
    },
    {
      user_id: ObjectId("user_id_2"),
      role: "member",
      joined_at: ISODate("2024-01-05"),
      contribution_score: 72,
      is_active: true
    }
  ],
  member_count: 4,
  max_members: 6,

  // Status
  is_private: false,
  requires_approval: true,
  is_active: true,
  status: "active",  // active, inactive, archived, completed

  // Schedule
  meeting_schedule: {
    frequency: "weekly",  // daily, weekly, biweekly, flexible
    regular_slots: [
      {
        day: "monday",
        start_time: "18:00",
        end_time: "20:00",
        timezone: "America/New_York"
      }
    ],
    next_meeting: ISODate("2024-01-22T18:00:00Z")
  },

  // Goals
  goals: [
    {
      description: "Complete coursework chapters 5-8",
      deadline: ISODate("2024-02-01"),
      status: "in_progress",  // pending, in_progress, completed
      completion_percentage: 60
    }
  ],

  // Compatibility & Performance
  compatibility_score: 87.5,  // Calculated by graph algorithm
  performance_metrics: {
    average_attendance_rate: 0.92,
    average_session_duration: 120,  // minutes
    total_sessions_completed: 15,
    total_study_hours: 45,
    group_productivity_score: 8.2,
    collaboration_effectiveness: 0.88,
    goal_completion_rate: 0.75
  },

  // Graph Algorithm Data
  graph_metrics: {
    average_pairwise_compatibility: 0.85,
    group_cohesion_score: 0.89,
    diversity_index: 0.65,
    optimal_size_achieved: true,
    rebalance_recommended: false
  },

  // Resources
  resources: [
    {
      title: "ML Lecture Notes",
      type: "document",
      url: "https://...",
      uploaded_by: ObjectId("user_id"),
      uploaded_at: ISODate("2024-01-10")
    }
  ],

  // Activity
  last_activity: ISODate("2024-01-20T19:30:00Z"),
  activity_score: 85,  // Based on recent engagement

  // Metadata
  created_at: ISODate("2024-01-01T10:00:00Z"),
  updated_at: ISODate("2024-01-20T19:30:00Z"),

  indexes: [
    { subject: 1 },
    { "members.user_id": 1 },
    { compatibility_score: -1 },
    { is_private: 1, is_active: 1 },
    { created_at: -1 }
  ]
}
```

### 3. study_sessions Collection

Records individual study sessions for analytics.

```javascript
{
  _id: ObjectId("..."),

  // Session Type
  session_type: "group",  // solo, pair, group, tutoring

  // Participants
  user_id: ObjectId("user_id"),  // Primary user (for solo sessions)
  participants: [ObjectId("user_id_1"), ObjectId("user_id_2")],
  group_id: ObjectId("group_id"),  // If group session

  // Session Details
  subject: "Machine Learning",
  topics_covered: ["Neural Networks", "Backpropagation"],

  // Timing
  start_time: ISODate("2024-01-20T18:00:00Z"),
  end_time: ISODate("2024-01-20T20:30:00Z"),
  duration_minutes: 150,
  scheduled_duration: 120,

  // Location/Platform
  location_type: "online",  // online, library, campus, other
  platform: "Zoom",
  meeting_link: "https://zoom.us/j/...",

  // Activities Logged
  activities: [
    {
      type: "reading",
      duration_minutes: 45,
      description: "Chapter 5 - Neural Networks"
    },
    {
      type: "problem_solving",
      duration_minutes: 60,
      problems_solved: 8
    },
    {
      type: "discussion",
      duration_minutes: 45
    }
  ],

  // Resources Used
  resources_used: [
    {
      type: "textbook",
      title: "Deep Learning by Goodfellow",
      pages: "Chapter 5"
    },
    {
      type: "video",
      title: "3Blue1Brown Neural Networks",
      url: "https://..."
    }
  ],

  // Session Quality
  productivity_rating: 8,  // 1-10 scale
  effectiveness_rating: 9,
  collaboration_rating: 8,  // For group sessions
  notes: "Covered backpropagation in detail. Need to review chain rule.",

  // Outcomes
  goals_achieved: [
    "Understand forward pass",
    "Implement simple neural network"
  ],
  follow_up_items: [
    "Review calculus for backprop",
    "Complete assignment 3"
  ],

  // Attendance (for group sessions)
  attendance: [
    {
      user_id: ObjectId("user_id_1"),
      attended: true,
      joined_at: ISODate("2024-01-20T18:00:00Z"),
      left_at: ISODate("2024-01-20T20:30:00Z")
    }
  ],

  // Metadata
  created_at: ISODate("2024-01-20T18:00:00Z"),
  updated_at: ISODate("2024-01-20T20:35:00Z"),

  indexes: [
    { user_id: 1, start_time: -1 },
    { group_id: 1, start_time: -1 },
    { "participants": 1 },
    { subject: 1, start_time: -1 },
    { start_time: -1 }
  ]
}
```

### 4. learning_patterns Collection

Daily aggregated learning data for ML analysis.

```javascript
{
  _id: ObjectId("..."),

  user_id: ObjectId("user_id"),
  date: ISODate("2024-01-20T00:00:00Z"),

  // Study Metrics
  total_study_duration: 240,  // minutes
  session_count: 3,
  average_session_duration: 80,

  // Timing Patterns
  study_times: [
    {
      start: "09:00",
      end: "11:00",
      productivity_score: 7
    },
    {
      start: "14:00",
      end: "16:00",
      productivity_score: 8
    },
    {
      start: "20:00",
      end: "21:20",
      productivity_score: 6
    }
  ],
  peak_productivity_hour: 14,
  time_of_day_distribution: {
    morning: 120,  // minutes
    afternoon: 120,
    evening: 80,
    night: 0
  },

  // Subject Distribution
  subjects_studied: [
    {
      subject: "Machine Learning",
      duration: 150,
      topics: ["Neural Networks", "Backpropagation"]
    },
    {
      subject: "Algorithms",
      duration: 90,
      topics: ["Dynamic Programming"]
    }
  ],

  // Activity Types
  activity_breakdown: {
    reading: 90,
    problem_solving: 100,
    video_watching: 30,
    discussion: 80,
    note_taking: 40
  },

  // Resource Usage
  resources_used: [
    {
      type: "textbook",
      count: 2,
      duration: 120
    },
    {
      type: "video",
      count: 3,
      duration: 45
    },
    {
      type: "interactive",
      count: 1,
      duration: 75
    }
  ],

  // Collaboration
  solo_study_time: 160,
  collaborative_study_time: 80,
  partners_studied_with: 2,
  group_study_time: 80,

  // Performance Indicators
  productivity_score: 7.8,  // 1-10
  focus_score: 8.2,
  comprehension_score: 7.5,
  problems_solved: 15,
  pages_read: 45,
  videos_watched: 3,

  // Behavioral Patterns
  break_frequency: 4,  // Number of breaks
  average_break_duration: 15,  // minutes
  distraction_count: 3,
  consistency_score: 8.5,

  // Clustering Features (for ML)
  feature_vector: [7.8, 14, 3, 240, 0.33, 8.2, 2],
  // [productivity, peak_hour, session_count, total_duration,
  //  collaboration_ratio, focus_score, resource_diversity]

  cluster_label: 2,

  // Metadata
  created_at: ISODate("2024-01-20T23:59:59Z"),
  updated_at: ISODate("2024-01-20T23:59:59Z"),

  indexes: [
    { user_id: 1, date: -1 },
    { date: -1 },
    { cluster_label: 1 },
    { user_id: 1, cluster_label: 1 }
  ]
}
```

### 5. recommendations Collection

Stores generated recommendations and user feedback.

```javascript
{
  _id: ObjectId("..."),

  user_id: ObjectId("user_id"),

  recommendation_type: "study_partner",
  // Types: study_partner, study_group, resource, study_time, subject

  // Recommended Item
  recommended_item: {
    item_id: ObjectId("recommended_user_or_group_id"),
    item_type: "user",  // user, group, resource, time_slot
    item_data: {
      // For user recommendations
      name: "Jane Smith",
      major: "Computer Science",
      year: 3,
      shared_subjects: ["Machine Learning", "Algorithms"],
      // For group recommendations
      group_name: "ML Study Group",
      member_count: 4
    }
  },

  // Scoring
  score: 87.5,  // Recommendation confidence score (0-100)
  rank: 3,  // Position in recommendation list

  // Algorithm Details
  algorithm_used: "collaborative_filtering",
  // Algorithms: similarity_matching, collaborative_filtering,
  //             content_based, hybrid, graph_based

  algorithm_details: {
    similarity_score: 0.875,
    common_interests: 5,
    schedule_overlap: 0.75,
    learning_pace_match: 0.90,
    past_collaboration_success: null
  },

  // Explanation (for user interface)
  explanation: "Matched based on similar learning pace and shared interest in ML",
  explanation_factors: [
    {
      factor: "learning_pace",
      weight: 0.3,
      score: 0.90,
      description: "Both prefer moderate learning pace"
    },
    {
      factor: "subject_overlap",
      weight: 0.25,
      score: 0.85,
      description: "5 shared subjects of interest"
    }
  ],

  // User Interaction
  shown_to_user: true,
  shown_at: ISODate("2024-01-20T15:00:00Z"),
  user_action: "accepted",  // null, viewed, accepted, rejected, ignored
  action_timestamp: ISODate("2024-01-20T15:05:00Z"),
  user_feedback: {
    rating: 5,  // 1-5 stars
    feedback_text: "Great match! Very helpful study partner.",
    would_recommend: true
  },

  // A/B Testing
  experiment_id: "rec_algo_test_v2",
  variant: "A",

  // Context
  context: {
    user_page: "find_partners",
    search_query: "machine learning",
    filters_applied: ["same_institution", "similar_level"],
    time_of_day: "afternoon",
    day_of_week: "monday"
  },

  // Metadata
  created_at: ISODate("2024-01-20T15:00:00Z"),
  expires_at: ISODate("2024-01-27T15:00:00Z"),  // Recommendation validity
  updated_at: ISODate("2024-01-20T15:05:00Z"),

  indexes: [
    { user_id: 1, created_at: -1 },
    { user_id: 1, recommendation_type: 1, user_action: 1 },
    { "recommended_item.item_id": 1 },
    { score: -1 },
    { expires_at: 1 }  // For TTL cleanup
  ]
}
```

### 6. achievements Collection

Defines available achievements/badges in the system.

```javascript
{
  _id: ObjectId("..."),

  // Basic Info
  name: "Study Streak Champion",
  description: "Maintain a 30-day study streak",

  // Visual
  icon_url: "https://.../icons/streak_champion.png",
  icon_name: "streak_fire",
  color: "#FF6B6B",

  // Type & Category
  type: "badge",  // badge, milestone, challenge, title
  category: "engagement",  // engagement, performance, collaboration, mastery

  // Difficulty
  tier: "gold",  // bronze, silver, gold, platinum, legendary
  rarity: "rare",  // common, uncommon, rare, epic, legendary
  difficulty: "hard",  // easy, medium, hard, expert

  // Criteria
  criteria: {
    metric: "study_streak_days",
    operator: ">=",
    threshold: 30,
    additional_conditions: [
      {
        metric: "min_daily_study_minutes",
        operator: ">=",
        threshold: 30
      }
    ]
  },

  // Rewards
  rewards: {
    points: 500,
    experience: 1000,
    special_title: "Streak Champion",
    unlocks: ["special_badge_showcase"]
  },

  // Progression
  has_levels: true,
  levels: [
    {
      level: 1,
      name: "Streak Starter",
      threshold: 7,
      points: 100
    },
    {
      level: 2,
      name: "Streak Builder",
      threshold: 15,
      points: 250
    },
    {
      level: 3,
      name: "Streak Champion",
      threshold: 30,
      points: 500
    }
  ],

  // Visibility
  is_active: true,
  is_secret: false,  // Hidden until unlocked
  is_limited_time: false,
  available_from: ISODate("2024-01-01"),
  available_until: null,

  // Stats
  times_earned: 234,
  percentage_of_users: 12.5,
  average_days_to_earn: 45,

  // Metadata
  created_at: ISODate("2024-01-01"),
  updated_at: ISODate("2024-01-15"),

  indexes: [
    { name: 1 },
    { category: 1, tier: 1 },
    { is_active: 1 },
    { "criteria.metric": 1 }
  ]
}
```

### 7. messages Collection

Stores chat messages between users.

```javascript
{
  _id: ObjectId("..."),

  // Participants
  sender_id: ObjectId("user_id_1"),
  receiver_id: ObjectId("user_id_2"),  // null for group messages
  group_id: ObjectId("group_id"),  // null for direct messages

  // Message Type
  message_type: "text",  // text, image, file, link, system

  // Content
  content: "Hey, want to study ML together tomorrow?",
  formatted_content: "<p>Hey, want to study ML together tomorrow?</p>",

  // Attachments
  attachments: [
    {
      type: "file",
      filename: "notes.pdf",
      url: "https://.../files/notes.pdf",
      size: 2048576,  // bytes
      mime_type: "application/pdf"
    }
  ],

  // Status
  is_read: false,
  read_at: null,
  is_delivered: true,
  delivered_at: ISODate("2024-01-20T15:00:05Z"),

  // Reactions
  reactions: [
    {
      user_id: ObjectId("user_id_2"),
      emoji: "👍",
      reacted_at: ISODate("2024-01-20T15:01:00Z")
    }
  ],

  // Threading
  reply_to: ObjectId("message_id"),  // For threaded replies
  thread_count: 3,

  // Moderation
  is_edited: false,
  edited_at: null,
  is_deleted: false,
  deleted_at: null,

  // Metadata
  timestamp: ISODate("2024-01-20T15:00:00Z"),
  created_at: ISODate("2024-01-20T15:00:00Z"),
  updated_at: ISODate("2024-01-20T15:00:00Z"),

  indexes: [
    { sender_id: 1, receiver_id: 1, timestamp: -1 },
    { group_id: 1, timestamp: -1 },
    { receiver_id: 1, is_read: 1 },
    { timestamp: -1 }
  ]
}
```

### 8. partner_requests Collection

Tracks study partner connection requests.

```javascript
{
  _id: ObjectId("..."),

  // Request Details
  requester_id: ObjectId("user_id_1"),
  requestee_id: ObjectId("user_id_2"),

  // Status
  status: "pending",  // pending, accepted, rejected, cancelled, expired

  // Message
  message: "Hi! I saw we're both studying ML. Want to be study partners?",

  // Recommendation Context
  from_recommendation: true,
  recommendation_id: ObjectId("recommendation_id"),
  match_score: 87.5,

  // Response
  response_message: null,
  responded_at: null,

  // Metadata
  created_at: ISODate("2024-01-20T14:00:00Z"),
  updated_at: ISODate("2024-01-20T14:00:00Z"),
  expires_at: ISODate("2024-01-27T14:00:00Z"),  // Auto-expire after 7 days

  indexes: [
    { requester_id: 1, status: 1 },
    { requestee_id: 1, status: 1 },
    { status: 1, created_at: -1 },
    { expires_at: 1 }  // For TTL cleanup
  ]
}
```

## Relationships Between Collections

```
users (1) -----> (N) study_sessions
users (N) <----> (N) study_groups (via members array)
users (1) -----> (N) learning_patterns
users (1) -----> (N) recommendations
users (N) <----> (N) users (study partners)
users (1) -----> (N) messages (sender)
users (1) -----> (N) messages (receiver)
users (N) -----> (N) achievements (via gamification.badges)

study_groups (1) -----> (N) study_sessions
study_groups (1) -----> (N) messages

recommendations -----> users (recommended_item)
recommendations -----> study_groups (recommended_item)

partner_requests (N) -----> (1) users (requester)
partner_requests (N) -----> (1) users (requestee)
```

## Indexing Strategy

### Primary Indexes
- All `_id` fields (automatic)
- Unique indexes: `users.email`, `users.username`

### Query Optimization Indexes
- Compound indexes for frequent queries
- Indexes on foreign keys (user_id, group_id)
- Indexes on status fields for filtering
- Indexes on timestamp fields for sorting

### Text Search Indexes
```javascript
// users collection
db.users.createIndex({
  "profile.full_name": "text",
  "profile.bio": "text",
  "profile.subjects_of_interest": "text"
})

// study_groups collection
db.study_groups.createIndex({
  name: "text",
  description: "text",
  subject: "text",
  tags: "text"
})
```

## Data Retention & Archiving

### Active Data
- **users**: Indefinite (until account deletion)
- **study_groups**: Active + 6 months after last activity
- **study_sessions**: 2 years
- **learning_patterns**: 2 years
- **recommendations**: 30 days (TTL index)
- **messages**: 1 year
- **partner_requests**: 30 days (TTL index)

### Archiving Strategy
- Move old sessions/patterns to archive collection
- Compress archived data
- Keep aggregated statistics

## Performance Considerations

1. **Embedding vs Referencing**:
   - Embed: Small, frequently accessed together data
   - Reference: Large arrays, many-to-many relationships

2. **Denormalization**:
   - Store computed values (scores, counts) to avoid expensive queries
   - Update denormalized data asynchronously via Celery

3. **Caching**:
   - Cache frequently accessed data (user profiles, leaderboards)
   - Cache expensive analytics queries
   - Use Redis for caching layer

4. **Aggregation Pipelines**:
   - Use for complex analytics queries
   - Pre-compute and cache results
   - Run heavy computations during off-peak hours

## Backup Strategy

1. **Daily Backups**: Full database backup every 24 hours
2. **Point-in-Time Recovery**: Enable MongoDB oplog
3. **Backup Retention**: Keep daily backups for 30 days
4. **Testing**: Monthly restore tests

---

**Document Version**: 1.0
**Last Updated**: January 2024
