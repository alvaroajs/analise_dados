from limpeza_dados import executar_limpeza
from respostas_case import responder_perguntas_pdf


from metrics_financeiras import gerar_visao_geografica
from metrics_qualidade import gerar_visao_fornecedores
from metrics_lucratividade import gerar_visao_lucratividade

def main():
    print("\n" + "="*50)
    print(" PIPELINE DE DADOS ")
    print("="*50 + "\n")
    
    try:  
        executar_limpeza()         
        responder_perguntas_pdf()  
        
        
        print("\n>>> GERANDO BASES DE PARA O BI")
        gerar_visao_geografica()
        gerar_visao_fornecedores()
        gerar_visao_lucratividade()

        print("\n" + "="*50)
        print(" Respostas no terminal e arquivos na data/processed/")
        print("="*50 + "\n")

    except Exception as e:
        print(f"\n❌ ERRO DURANTE O PIPELINE: {e}")

if __name__ == "__main__":
    main()