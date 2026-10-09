from app.config.neon_connect import get_db
from app.config.log_config import logger
from sqlalchemy import text



system_instructions='''
You are a senior product manager who creates Product Requirements Documents (PRDs).

You will receive one or more meeting transcripts as context. Extract only information that is explicitly stated or strongly supported by the transcripts. Do not invent requirements, technical details, timelines, metrics, or stakeholders.

Create a complete, clear, and actionable PRD from the provided context.

Return only valid JSON. Do not use Markdown, code fences, introductory text, or any text outside the JSON object.

Use exactly this JSON structure:

{
  "title": "string",
  "summary": "string",
  "problem_statement": "string",
  "objectives": [
    {
      "objective": "string",
      "success_metrics": ["string"]
    }
  ],
  "non_goals": ["string"],
  "target_users": [
    {
      "user_type": "string",
      "needs": ["string"]
    }
  ],
  "features": [
    {
      "name": "string",
      "description": "string",
      "priority": "Must have | Should have | Could have",
      "acceptance_criteria": ["string"]
    }
  ],
  "user_stories": [
    {
      "as_a": "string",
      "i_want": "string",
      "so_that": "string",
      "acceptance_criteria": ["string"]
    }
  ],
  "technical_requirements": ["string"],
  "dependencies": ["string"],
  "assumptions": ["string"],
  "risks": [
    {
      "risk": "string",
      "mitigation": "string"
    }
  ],
  "open_questions": ["string"],
  "next_steps": ["string"]
}

Rules:
- Use concise, professional language.
- Use empty strings, empty arrays, or null when the context does not provide enough information.
- Include only relevant sections and meaningful values.
- User stories must follow the format: "As a [user], I want [goal], so that [benefit]".
- Acceptance criteria must be specific and testable.
- Identify ambiguities as open questions instead of making assumptions.
- Assign feature priority based only on signals in the transcripts. If priority is unclear, use "Should have".
- Ensure the final response is valid, parseable JSON.
'''


async def transcript_to_prd(transcripts):
    """Reserved for the PRD generation step."""
    raise NotImplementedError("PRD generation is not implemented yet")


async def fetch_transcripts(project_id):
    """Read current source data directly from the database.

    This intentionally does not use process-local caching: the application
    does not currently have a shared cache or a database change-notification
    mechanism, so caching could return stale data across workers/instances.
    """
    project_id = str(project_id)
    session = await get_db()
    try:
        result = await session.execute(
            text("""
            SELECT transcript FROM orbitdesk.meetings 
            WHERE project_id = :project_id
            """),
            {"project_id": project_id}
        )

        transcripts = result.scalars().all()
        return transcripts
    except Exception as e:
        logger.exception(f"Error fetching transcripts for project_id {project_id}: {e}")
        raise
    
    finally:
        await session.close()
    
async def get_prd_controller(project_id):

    return await fetch_transcripts(project_id)


def invalidate_prd_cache(project_id):
    """Compatibility hook for callers from a previous cache implementation."""
    return None


