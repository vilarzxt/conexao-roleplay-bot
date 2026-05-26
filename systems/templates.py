import discord

from config.assets import (
    EMBED_COLOR,
    ASSETS
)

from systems.utils import (
    create_embed
)

# =========================
# 🎫 TICKET TEMPLATES
# V1.3.2
# =========================

def get_ticket_template(
    subcategory: str
):

    # =========================
    # 🚨 DENÚNCIAS
    # =========================

    if subcategory == "denuncia_player":

        embed = create_embed(

            title="🚨 Denúncia contra Player",

            description=(
                "Preencha corretamente "
                "as informações abaixo "
                "para prosseguir com "
                "a denúncia."
            ),

            color=EMBED_COLOR
        )

        embed.add_field(

            name="📋 Informações Necessárias",

            value=(
                "• Nick do jogador\n"
                "• ID do jogador\n"
                "• Motivo da denúncia\n"
                "• Data e horário\n"
                "• Link das provas\n"
                "• Informações adicionais"
            ),

            inline=False
        )

    elif subcategory == "denuncia_staff":

        embed = create_embed(

            title="👮 Denúncia contra Staff",

            description=(
                "Envie todas as informações "
                "necessárias para análise "
                "da equipe administrativa."
            ),

            color=EMBED_COLOR
        )

        embed.add_field(

            name="📋 Informações Necessárias",

            value=(
                "• Nome da staff\n"
                "• Cargo\n"
                "• Motivo\n"
                "• Data e horário\n"
                "• Link das provas\n"
                "• Informações adicionais"
            ),

            inline=False
        )

    elif subcategory == "denuncia_organizacao":

        embed = create_embed(

            title="🏢 Denúncia contra Organização",

            description=(
                "Informe corretamente "
                "os dados da organização "
                "envolvida."
            ),

            color=EMBED_COLOR
        )

        embed.add_field(

            name="📋 Informações Necessárias",

            value=(
                "• Nome da organização\n"
                "• Integrantes envolvidos\n"
                "• Ocorrido\n"
                "• Data e horário\n"
                "• Link das provas"
            ),

            inline=False
        )

    # =========================
    # ❓ DÚVIDAS
    # =========================

    elif subcategory == "duvidas_gerais":

        embed = create_embed(

            title="❓ Dúvidas Gerais",

            description=(
                "Descreva sua dúvida "
                "com o máximo de detalhes."
            ),

            color=EMBED_COLOR
        )

    elif subcategory == "suporte_tecnico":

        embed = create_embed(

            title="🛠️ Suporte Técnico",

            description=(
                "Informe o problema "
                "técnico encontrado."
            ),

            color=EMBED_COLOR
        )

        embed.add_field(

            name="📋 Informações Necessárias",

            value=(
                "• Plataforma\n"
                "• Problema encontrado\n"
                "• Frequência do problema\n"
                "• Sistema afetado\n"
                "• Prints ou vídeos"
            ),

            inline=False
        )

    # =========================
    # 💰 FINANCEIRO
    # =========================

    elif subcategory == "vip_coins":

        embed = create_embed(

            title="💳 VIP ou Problemas com Coins",

            description=(
                "Envie as informações "
                "financeiras corretamente."
            ),

            color=EMBED_COLOR
        )

        embed.add_field(

            name="📋 Informações Necessárias",

            value=(
                "• ID da compra\n"
                "• Produto adquirido\n"
                "• Comprovante\n"
                "• ID do jogador"
            ),

            inline=False
        )

    elif subcategory == "problemas_financeiros":

        embed = create_embed(

            title="⚠️ Problemas Financeiros",

            description=(
                "Descreva o problema "
                "financeiro ocorrido."
            ),

            color=EMBED_COLOR
        )

        embed.add_field(

            name="📋 Informações Necessárias",

            value=(
                "• Problema ocorrido\n"
                "• ID da conta\n"
                "• Data do ocorrido\n"
                "• Prints ou provas"
            ),

            inline=False
        )

    # =========================
    # 🏢 ORGANIZAÇÕES
    # =========================

    elif subcategory == "marcar_acoes":

        embed = create_embed(

            title="🎯 Marcar Ações",

            description=(
                "Preencha as informações "
                "da ação organizacional."
            ),

            color=EMBED_COLOR
        )

    elif subcategory == "suporte_org":

        embed = create_embed(

            title="🏢 Suporte Organizacional",

            description=(
                "Informe o problema "
                "relacionado à organização."
            ),

            color=EMBED_COLOR
        )

    elif subcategory == "duvidas_org":

        embed = create_embed(

            title="❓ Dúvidas Organizacionais",

            description=(
                "Envie sua dúvida "
                "organizacional."
            ),

            color=EMBED_COLOR
        )

    # =========================
    # 🤝 PARCERIAS
    # =========================

    elif subcategory == "criadores":

        embed = create_embed(

            title="🎥 Criadores de Conteúdo",

            description=(
                "Envie suas informações "
                "para análise de parceria."
            ),

            color=EMBED_COLOR
        )

        embed.add_field(

            name="📋 Informações Necessárias",

            value=(
                "• Canal ou rede social\n"
                "• Estatísticas\n"
                "• Tipo de conteúdo\n"
                "• ID in-game"
            ),

            inline=False
        )

    elif subcategory == "projetos_servidores":

        embed = create_embed(

            title="🤝 Projetos / Servidores",

            description=(
                "Envie sua proposta "
                "de parceria."
            ),

            color=EMBED_COLOR
        )

    elif subcategory == "duvidas_parceria":

        embed = create_embed(

            title="❓ Dúvidas de Parceria",

            description=(
                "Envie sua dúvida "
                "sobre parcerias."
            ),

            color=EMBED_COLOR
        )

    # =========================
    # ⚠️ DEFAULT
    # =========================

    else:

        embed = create_embed(

            title="🎫 Ticket",

            description=(
                "Seu ticket foi criado."
            ),

            color=EMBED_COLOR
        )

    # =========================
    # 🖼️ BANNER
    # =========================

    embed.set_image(
        url=ASSETS["banner_ticket"]
    )

    return embed
