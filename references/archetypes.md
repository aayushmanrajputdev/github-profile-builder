# Developer Archetypes

This document describes the different developer archetypes supported by github-profile-builder.

## Available Archetypes

1. **Developer** (default) - General purpose, showcases coding activity and repositories
2. **Open Source Contributor** - Highlights open source contributions and community impact
3. **Data Scientist** - Emphasizes data science projects, Python/R usage, and ML contributions
4. **Student/Learner** - Focuses on learning progress, practice repositories, and growth streaks
5. **Creator** - Showcases diverse skills, personal projects, and creative outputs

## Archetype Selection

Use `--archetype <name>` to select an archetype. Each archetype emphasizes different aspects:

| Archetype | Strengths Emphasized | Color Theme |
|-----------|---------------------|-------------|
| Developer | Repositories, Streaks, Code | Blue tones |
| Open Source | Contributions, PRs, Issues | Green tones |
| Data Scientist | Languages, Projects, Stats | Orange/Amber |
| Student | Learning, Practice, Growth | Purple tones |
| Creator | Diversity, Creativity, Links | Rainbow/Accent |

## Default Behavior

If no archetype is specified, "developer" is used as the default.

## Implementation

Archetypes affect:
- README.md structure and emphasis
- Color palette recommendations
- Highlighted metrics
- Profile section ordering