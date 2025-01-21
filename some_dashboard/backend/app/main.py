import uvicorn

from infrastructure.bootstrap import bootstrap_db
from entrypoints.fastapi import create_app
from settings import settings

if __name__ == "__main__":
    bootstrap_db()
    uvicorn.run(
        create_app(),
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        access_log=False,
        reload_dirs=["templates", "static"],
    )
