#!/bin/bash
# 📋 Script pour documenter le nettoyage dans Git

echo "📚 GIT - Ajout des nouveaux fichiers de documentation"
echo "========================================================="

git add STRUCTURE_PROPRE.md
git add ARCHITECTURE_REORGANISEE.md
git add README_NEW.md
git add VALIDATION_NETTOYAGE.md
git add RESUME_NETTOYAGE_FINAL.md
git add CHEMINS_ET_IMPORTS.md
git add INDEX_NETTOYAGE.md
git add cleanup_obsolete.sh

echo "✅ Fichiers ajoutés au staging"
echo ""
echo "📝 Créer le commit avec:"
echo "   git commit -m '🧹 Nettoyage de printemps v3.1.0 - Réorganisation architecture'"
echo ""
echo "📤 Pousser vers origin avec:"
echo "   git push origin main"
echo ""
echo "========================================================="
