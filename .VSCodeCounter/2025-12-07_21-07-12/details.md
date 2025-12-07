# Details

Date : 2025-12-07 21:07:12

Directory e:\\VSProjects\\AINovel\\ainovel

Total : 91 files,  13565 codes, 468 comments, 827 blanks, all 14860 lines

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [.claude/settings.local.json](/.claude/settings.local.json) | JSON | 13 | 0 | 1 | 14 |
| [.prettierrc.json](/.prettierrc.json) | JSON | 5 | 0 | 1 | 6 |
| [README.md](/README.md) | Markdown | 30 | 0 | 14 | 44 |
| [backend/.env](/backend/.env) | Dotenv | 10 | 2 | 2 | 14 |
| [backend/README.md](/backend/README.md) | Markdown | 23 | 0 | 9 | 32 |
| [backend/alembic.ini](/backend/alembic.ini) | Ini | 104 | 0 | 24 | 128 |
| [backend/app/\_\_init\_\_.py](/backend/app/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [backend/app/api/\_\_init\_\_.py](/backend/app/api/__init__.py) | Python | 2 | 0 | 1 | 3 |
| [backend/app/api/ai.py](/backend/app/api/ai.py) | Python | 280 | 16 | 27 | 323 |
| [backend/app/api/auth.py](/backend/app/api/auth.py) | Python | 110 | 2 | 18 | 130 |
| [backend/app/api/novels.py](/backend/app/api/novels.py) | Python | 148 | 27 | 20 | 195 |
| [backend/app/core/\_\_init\_\_.py](/backend/app/core/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [backend/app/core/config.py](/backend/app/core/config.py) | Python | 15 | 2 | 5 | 22 |
| [backend/app/crud/\_\_init\_\_.py](/backend/app/crud/__init__.py) | Python | 2 | 0 | 1 | 3 |
| [backend/app/crud/crud\_novel.py](/backend/app/crud/crud_novel.py) | Python | 115 | 4 | 21 | 140 |
| [backend/app/db/\_\_init\_\_.py](/backend/app/db/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [backend/app/db/database.py](/backend/app/db/database.py) | Python | 13 | 0 | 2 | 15 |
| [backend/app/db/init\_db.py](/backend/app/db/init_db.py) | Python | 13 | 4 | 7 | 24 |
| [backend/app/main.py](/backend/app/main.py) | Python | 34 | 4 | 9 | 47 |
| [backend/app/models/\_\_init\_\_.py](/backend/app/models/__init__.py) | Python | 3 | 0 | 1 | 4 |
| [backend/app/models/novel.py](/backend/app/models/novel.py) | Python | 28 | 1 | 7 | 36 |
| [backend/app/models/user.py](/backend/app/models/user.py) | Python | 12 | 0 | 2 | 14 |
| [backend/app/models/vector.py](/backend/app/models/vector.py) | Python | 17 | 0 | 3 | 20 |
| [backend/app/schemas/\_\_init\_\_.py](/backend/app/schemas/__init__.py) | Python | 9 | 0 | 1 | 10 |
| [backend/app/schemas/ai.py](/backend/app/schemas/ai.py) | Python | 33 | 1 | 5 | 39 |
| [backend/app/schemas/novel.py](/backend/app/schemas/novel.py) | Python | 58 | 1 | 14 | 73 |
| [backend/app/schemas/user.py](/backend/app/schemas/user.py) | Python | 19 | 0 | 5 | 24 |
| [backend/app/services/\_\_init\_\_.py](/backend/app/services/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [backend/app/services/ai\_service.py](/backend/app/services/ai_service.py) | Python | 206 | 20 | 35 | 261 |
| [backend/app/services/vector\_service.py](/backend/app/services/vector_service.py) | Python | 143 | 16 | 28 | 187 |
| [backend/debug\_write.py](/backend/debug_write.py) | Python | 60 | 6 | 5 | 71 |
| [backend/init\_db.py](/backend/init_db.py) | Python | 62 | 9 | 14 | 85 |
| [backend/init\_db\_simple.py](/backend/init_db_simple.py) | Python | 13 | 1 | 5 | 19 |
| [backend/insert\_sample\_data\_final.py](/backend/insert_sample_data_final.py) | Python | 56 | 4 | 12 | 72 |
| [backend/requirements.txt](/backend/requirements.txt) | pip requirements | 20 | 0 | 0 | 20 |
| [backend/reset\_data.py](/backend/reset_data.py) | Python | 84 | 4 | 10 | 98 |
| [backend/sql/01\_create\_database.sql](/backend/sql/01_create_database.sql) | MS SQL | 3 | 3 | 2 | 8 |
| [backend/sql/02\_create\_tables.sql](/backend/sql/02_create_tables.sql) | MS SQL | 68 | 11 | 13 | 92 |
| [backend/sql/03\_sample\_data.sql](/backend/sql/03_sample_data.sql) | MS SQL | 46 | 7 | 24 | 77 |
| [backend/sql/04\_update\_novel\_embeddings\_metadata\_column.sql](/backend/sql/04_update_novel_embeddings_metadata_column.sql) | MS SQL | 2 | 3 | 2 | 7 |
| [backend/sql/README.md](/backend/sql/README.md) | Markdown | 65 | 0 | 27 | 92 |
| [backend/test\_ai\_write.py](/backend/test_ai_write.py) | Python | 30 | 6 | 6 | 42 |
| [backend/test\_api.py](/backend/test_api.py) | Python | 37 | 8 | 7 | 52 |
| [backend/test\_db\_connection.py](/backend/test_db_connection.py) | Python | 45 | 8 | 10 | 63 |
| [backend/test\_db\_simple.py](/backend/test_db_simple.py) | Python | 60 | 10 | 15 | 85 |
| [backend/test\_db\_sync.py](/backend/test_db_sync.py) | Python | 53 | 8 | 13 | 74 |
| [backend/test\_real\_write.py](/backend/test_real_write.py) | Python | 38 | 8 | 9 | 55 |
| [backend/test\_write\_simple.py](/backend/test_write_simple.py) | Python | 32 | 5 | 8 | 45 |
| [eslint.config.js](/eslint.config.js) | JavaScript | 49 | 24 | 11 | 84 |
| [index.html](/index.html) | HTML | 21 | 1 | 3 | 25 |
| [package-lock.json](/package-lock.json) | JSON | 8,880 | 0 | 1 | 8,881 |
| [package.json](/package.json) | JSON | 48 | 0 | 1 | 49 |
| [postcss.config.js](/postcss.config.js) | JavaScript | 17 | 9 | 4 | 30 |
| [quasar.config.ts](/quasar.config.ts) | TypeScript | 79 | 113 | 44 | 236 |
| [restart-frontend.bat](/restart-frontend.bat) | Batch | 16 | 3 | 4 | 23 |
| [run-dev-all.bat](/run-dev-all.bat) | Batch | 40 | 1 | 7 | 48 |
| [run-dev.bat](/run-dev.bat) | Batch | 3 | 0 | 0 | 3 |
| [run-frontend.bat](/run-frontend.bat) | Batch | 16 | 2 | 3 | 21 |
| [run\_test\_server.bat](/run_test_server.bat) | Batch | 20 | 0 | 3 | 23 |
| [src/App.vue](/src/App.vue) | vue | 5 | 0 | 2 | 7 |
| [src/assets/quasar-logo-vertical.svg](/src/assets/quasar-logo-vertical.svg) | XML | 15 | 0 | 0 | 15 |
| [src/boot/axios.ts](/src/boot/axios.ts) | TypeScript | 13 | 7 | 3 | 23 |
| [src/boot/i18n.ts](/src/boot/i18n.ts) | TypeScript | 18 | 8 | 8 | 34 |
| [src/components/EssentialLink.vue](/src/components/EssentialLink.vue) | vue | 24 | 0 | 4 | 28 |
| [src/components/ExampleComponent.vue](/src/components/ExampleComponent.vue) | vue | 32 | 0 | 6 | 38 |
| [src/components/models.ts](/src/components/models.ts) | TypeScript | 7 | 0 | 2 | 9 |
| [src/css/app.scss](/src/css/app.scss) | SCSS | 0 | 1 | 1 | 2 |
| [src/css/quasar.variables.scss](/src/css/quasar.variables.scss) | SCSS | 9 | 10 | 7 | 26 |
| [src/env.d.ts](/src/env.d.ts) | TypeScript | 7 | 0 | 1 | 8 |
| [src/i18n/en-US/index.ts](/src/i18n/en-US/index.ts) | TypeScript | 4 | 2 | 2 | 8 |
| [src/i18n/index.ts](/src/i18n/index.ts) | TypeScript | 4 | 0 | 2 | 6 |
| [src/layouts/MainLayout.vue](/src/layouts/MainLayout.vue) | vue | 167 | 1 | 20 | 188 |
| [src/pages/ChapterEditorPage.vue](/src/pages/ChapterEditorPage.vue) | vue | 360 | 7 | 41 | 408 |
| [src/pages/ErrorNotFound.vue](/src/pages/ErrorNotFound.vue) | vue | 20 | 0 | 4 | 24 |
| [src/pages/IndexPage.vue](/src/pages/IndexPage.vue) | vue | 40 | 0 | 4 | 44 |
| [src/pages/LoginPage.vue](/src/pages/LoginPage.vue) | vue | 225 | 1 | 20 | 246 |
| [src/pages/NovelCreatePage.vue](/src/pages/NovelCreatePage.vue) | vue | 96 | 0 | 9 | 105 |
| [src/pages/NovelDetailPage.vue](/src/pages/NovelDetailPage.vue) | vue | 402 | 7 | 44 | 453 |
| [src/pages/NovelListPage.vue](/src/pages/NovelListPage.vue) | vue | 216 | 2 | 22 | 240 |
| [src/router/index.ts](/src/router/index.ts) | TypeScript | 21 | 12 | 7 | 40 |
| [src/router/routes.ts](/src/router/routes.ts) | TypeScript | 18 | 3 | 4 | 25 |
| [src/services/aiService.ts](/src/services/aiService.ts) | TypeScript | 57 | 1 | 10 | 68 |
| [src/services/authService.ts](/src/services/authService.ts) | TypeScript | 50 | 15 | 11 | 76 |
| [src/services/novelService.ts](/src/services/novelService.ts) | TypeScript | 71 | 0 | 14 | 85 |
| [src/stores/auth-store.ts](/src/stores/auth-store.ts) | TypeScript | 38 | 8 | 9 | 55 |
| [src/stores/example-store.ts](/src/stores/example-store.ts) | TypeScript | 17 | 0 | 5 | 22 |
| [src/stores/index.ts](/src/stores/index.ts) | TypeScript | 10 | 17 | 6 | 33 |
| [test\_ai\_write\_frontend.html](/test_ai_write_frontend.html) | HTML | 130 | 0 | 16 | 146 |
| [test\_api\_write.bat](/test_api_write.bat) | Batch | 21 | 0 | 3 | 24 |
| [test\_server.py](/test_server.py) | Python | 54 | 12 | 9 | 75 |
| [tsconfig.json](/tsconfig.json) | JSON with Comments | 6 | 0 | 1 | 7 |

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)