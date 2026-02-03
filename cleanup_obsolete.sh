#!/bin/bash
# 🧹 Script de nettoyage - Supprime les fichiers obsolètes

echo "🧹 NETTOYAGE DE PRINTEMPS - POC_MFE_2026"
echo "=========================================="
echo ""

# Compteurs
deleted=0
total=0

# Fonction pour supprimer un fichier
delete_file() {
    local file=$1
    local reason=$2
    if [ -f "$file" ]; then
        rm "$file"
        echo "✂️  Supprimé: $file ($reason)"
        ((deleted++))
    fi
    ((total++))
}

# Fonction pour supprimer un dossier
delete_dir() {
    local dir=$1
    local reason=$2
    if [ -d "$dir" ]; then
        rm -rf "$dir"
        echo "✂️  Supprimé: $dir ($reason)"
        ((deleted++))
    fi
    ((total++))
}

echo "📝 Suppression du code Python obsolète..."
delete_file "pages.py" "remplacé par page_functions.py"
delete_file "pages.py.backup" "backup obsolète"
delete_file "pages.py.new" "version test"
delete_file "examples_social_auth.py" "dupliqué dans page_social_linking.py"
delete_file "api_examples.py" "exemples obsolètes"
delete_file "apps_script_api.py" "Apps Script abandonné"
delete_file "google_sheets.py" "intégré dans backend_database.py"
delete_file "test_apps_script.py" "tests Apps Script"
delete_file "test_config.py" "tests inutiles"
delete_file "PROJECT_STATUS.py" "vieux fichier"

echo ""
echo "🚀 Suppression des scripts redondants..."
delete_file "start.bat" "remplacé par quickstart.sh"
delete_file "start.sh" "redondant"
delete_file "start_streamlit_fixed.py" "obsolète"
delete_file "launch_ngrok.py" "pas utilisé"
delete_file "launch_fixed.sh" "obsolète"

echo ""
echo "📚 Suppression de la documentation obsolète..."
delete_file "DEMARRAGE_RAPIDE_ETAPE_2.md" "remplacé par DEMARRAGE.md"
delete_file "ETAPE_2_RESUME.md" "résumé ancien"
delete_file "INDEX_ETAPE_2.md" "index ancien"
delete_file "INDEX_SIMPLE.md" "redondant"
delete_file "FLUX_VISUEL_ETAPE_2.md" "visuel ancien"
delete_file "SYNTHESE_ETAPE_2.txt" "synthèse ancienne"
delete_file "FIX_TIMEOUT.md" "issue résolue"
delete_file "CHECKLIST_SOCIAL_AUTH.md" "checklist ancienne"
delete_file "SETUP_APPS_SCRIPT.md" "Apps Script abandonné"
delete_file "BACKEND_MIGRATION.md" "migration ancienne"
delete_file "MIGRATION_SUMMARY.md" "résumé ancien"
delete_file "COMPLETION.md" "vieux status"
delete_file "POUR_L_UTILISATEUR.md" "doc ancienne"
delete_file "VERIFICATION_ET_RESUMÉ.txt" "vérif ancienne"
delete_file "RECAP_FINAL.txt" "recap ancien"
delete_file "RESUME_POUR_VOUS.md" "résumé ancien"
delete_file "ROADMAP.md" "roadmap ancienne"

echo ""
echo "🔧 Suppression du code Apps Script..."
delete_file "Code.gs" "Apps Script"
delete_file "APPS_SCRIPT_OPTIMIZED.gs" "Apps Script optimisé"

echo ""
echo "=========================================="
echo "✅ NETTOYAGE TERMINÉ"
echo "   Fichiers supprimés: $deleted/$total"
echo "=========================================="
echo ""
echo "📂 Structure nettoyée et organisée!"
echo "🚀 Prêt pour production!"
